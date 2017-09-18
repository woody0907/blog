[TOC]
##Data Flow
### Anatomy of File Write

It is instructive to understand the data flow becuase it clarifes HDFS's **coherency model**

- client create file by call create() on **DistributedFileSystem**
- **DistributedFileSys** make an RPC call to the namenode to create a new file in the filesystem's namespace. the namenode performs various check to make sure the file doesn't already exist and the client has the right permission to creat the file.
- DistrubutedFileSystem return an **DFSOutputStream** for the client to start writing data to. **FSDataOutputStream** wraps DFSOutputStream, which handles communications between datanodes and namenodes
- As client write data, the DFSOutputStream splite it into packets, which it writes to an internal queue called the data queue. The data queue is consumed by the **DataStreamer**, which is responsible for asking the namenode to allocate new blocks by picking a list of suitable datanodes to store the replicas.
 The list of datanode forms a pipeline, the DataStreamer streams the packets to the first datanode in the pipeline, which stores each packet and forwards it to the second datanode in the pipeline.
- The DFSOutputStream maintains an internal queue of packets that are waiting to be acknowledged by datanode, call the *ack queue*. A packet is remove from the ack queue only when it has been acknowledged by all the datanodes in the pipline.
- when the client has finished writing data it call close() on the stream. This action flushes all the remaining packets to the datanode pipline and waits for acknowledgement before contacting the namenode to signal that the file is complete.

#### Replica Replacement
> How does the namenode choose which datanodes to store replicas on?
There is a trade off between reliability and write bandwith and read bandwith, there are a variety of possible placement strategies, Hadoop's default strategy is to place the first replica on the same node as the client. The second replica is placed on a different rack(off rack) from the first (chosen at random). The third replica is place on the same rack as the second, but on a different node chosen at random.

### Coherency Mode
> Coherency mode for a filesystem describes the data visibility of reads and writes for a file.

After create a file, it is visible in the file namespace, however, any content written to the file is not guaranteed to be visible, even if the stream is flushed.
Once more than a block's worth of data has been written, the first block will be visible to new reader. it is always the current block being written that is not visible to other reader.
HDFS provides a way to force all buffers to be flushed to the datanodes via the hflush() method on FSDataOutputStream.

~~~java

	Path p = new Path("p");
	FSDataOutputStream out = fs.create(p);
	out.write("content".getByte("UTF-8"));
	out.hflush(); // 

	out.getFD().sync();//write data to filesystem
	out.close();//performs an implicit hflush();
~~~
Note that the hflush() doesn't guarantee that the datanode have written the data to disk, only that it's in the datanode's memory(data could be lost in the event of power outage).

### Parallel Copying with distcp

Hadoop comes with a useful program called distcp for copying data to and from Hadoop filesystems in parallel.

~~~
	% hadoop distcp file1 file2;
	% hadoop distcp dir1 dir2;
	% hadoop distcp -update dir1 dir2;
	//transferring data between two HDFS cluster
	% hadoop distcp -update -delete -p hdfs://namenode1/foo hdfd://namenode2/foo
	//if the two cluster are running imcompatible versions:
	% hadoop distcp webhdfs://namenode1:50070/foo webhdfs://namenode2:50070/foo
~~~

distcp is implemented as a MapReduce job where the work of copying is done by the maps that run in parallel across the cluster. There are no reduces.

## YARN
Apache YARN(yet another resource negotiator) is Hadoop's cluster resouce management system. It provides API for requesting and working with cluster resources,these API hide the resouce management details from other applications,such as Mapreduce, Spark, Tez and so on.

### Anatomy of a YARN Application Run
YARN provides its core services via two types of *long-running* daemon：a *resource manage*(one per cluster) to manage the use of resouces across the cluster, and *node managers* running on all the nodes in the cluster to launch and monitor containers.

### Resource Requests
Locality is critial in ensuring that distrubuted data processing algorithms use the cluster bandwidth efficiently, so YARN allow an application to specify locality constrains for the container it is requesting. Locality constrains can be used to request a container on a specific node or rack,or off-rack.

Sometimes the locality constrain cannot be met, optionally, the constrain can be loosened, then YARN will try to start container on a node in the same rack, or if that's impossible, on any node in the cluster.

*A YARN application can make resource request at any time* while it is running. for example, an application can make all of its request up front, or it can take a more dynamic approach whereby it requests more resources dynamically to meet the changing needs of the application.

Spark take the first approch, starting a fixed number of executors on the cluster. MapReduce, on the other hand, has two phases: the map task containers are requested up front, but the reduce task containers are not started until later. Also, if any tasks fail, additional containers will be requested so the fail tasks can be rerun.

### Application Lifespan
The lifespan of a YARN application can vary dramatically.

- The simplest case is one application per user job, which is the approch that **MapReduce takes**.

- The second model is to run one application per workflow or user session jobs. This can be more efficient than the first, since containers can be reused between jobs, and there is also the potential to cache intermediate data between jobs. **Spark is an example that use this model**.

- The third model is a long-running application that is shared by different user. Such as some application often acts in some kind of coordination role.

### Building YARN Application
Writing a YARN applicaiton from scratch is fairly involved, but im many case is not necessary, as it is often possible to use an existing application that fits the bill.

**Apache Slider** makes it possible to run existing distributed applications on YARN.

**Apache Twill** is similar to Slider, but in addition provides a simple programming mode for developing distributed applications on YARN. It also provides support for, among other things, real-time loggin.

**distributed shell application** that is a part of YARN project itself serves as an example of how to write YARN application.

### YARN Compared to MapReduce 1
The distributed implementation of MapReduce in the origianl version of Hadoop is sometimes referred to MapReduce1 to distinguish it from MapReduce2, the implementation that use YARN.

In Mapreduce1 there are two type of daemon that control the job execution process:*a jobtracker* and *one or more tasktracker*

In Mapreduce1 jobtracker takes care of both job scheduling and take progress monitoring, by contrast, in YARN these responsibilities are handled by seperate entities:*the resource manage and an application master*

Mapreduce 1 | YARN
---|---
jobtraker | resouce manager, application master,timeline server(store application history)
tasktraker | node manager
slot | container

the benifits to using YARN include the following:

- *Scalability*
YARN overcome scalability limitation by virtue of its split resource manager/application master architecture: it is design to scalp up to 10,000 nodes and 100,000 task.

- *Availability*
Provide HA for the resource manager and application master.

- *Utilization*
A node manager managers a pool of resources, rather than a fixed number of slot, furthermore, resouce in YARN are fine grained,so an application can take a request for what is needs.

- *Multitenancy*
In some ways, the biggest benifit of YARN is that it opens up Hadoop to other types of distribute applicaiton beyond Mapreduce. It is enen possible for users to run different version of Mapresuce on the same YARN cluster.

### Scheduling in YARN
It is the job of the YARN scheduler to allocate resources to applications according to some defined policy.

#### Scheduler options

There are three scheduler in YARN:

1. the FIFO
1. Capacity
1. Fair

FIFO Scheduler has the merit of being simple to understand and not needing any configuration, but it's not suitable for shared clusters.

With Capacity scheduler, a separate dedicated queue allows the small job to start as soon as it is submitted, although this is at the cost of overall cluster utiliaztion since the queue capacity is reserved for jobs in that queue.

With Fair Scheduler, there is no need to reserve a set amount of capacity, since it will dynamically balance resouces between all running jobs.

##Hadoop IO

###Data Integrity
the usual way of detecting corrupted data is by computing a checksum for the data when it first enters the system,this technique doesn't offer any way to fix the data, it is just error detection.

A commonly used error-detecting code is CRC-32, it is used for checksumming in Hadoop's *ChecksumFileSystem*, while HDFS use a more efficient variant called CRC-32C, which checksum is 4 bytes long, the stroage overhead is less than 1%.

###Data Integrity in HDFS

Datanodes are responsible for verifying the data they receive before storing the data and its checksum.

A client writing data sends it to pipeline of datanodes, and the last datanode verifies the checksum.

When client read data from datanodes, they verify checksums as well, comparing them with the ones stored at the datanodes. Each datanode keeps a persistent log of checksum verifications which is valuable in detecting bad disks.

In addition to block verification on client read,Each datanode runs a **DataBlockScaner** in a background thread that periodically verifies all the blocks stored on the datanode.

Because HDFS stores replica of blocks, it can heal corrupted blocks by copying one of the good replicas to produce a new, uncorrup replica.

It is possible to disable verifacation of checksum by passing false to the setVerifyChecksum() method on FileSystem before using the open() method to read a file. The same effect is possible from the shell by using the -ignoreCrc option with the -get or the equivalent -copyToLocal command.

You can find a file's checksum with dadoop fs -checksum. This is useful to check whether two files in HDFS have the same content.

###LocalFileSystem
The Hadoop LocalFileSystem performs client-side checksumming. The filesystem client creates hidden file .filename.crc transparently when you write a file called filename, in the same directory containing the checksums for each chunk of the file. the chunk size is controlled by the file.bytes-per-checksum property, which defaults to 521 bytes

It is possible to disable checksums, which is typically done when the underlying filesystem supports checksums natively. This is accomplished by using RawLocalFileSystem in place of LocalFileSystem. To do this globally in an application, it suffices to remap the impmentation for file URIs by setting the property fs.file.impl to the value RawLocalFileSystem.

###CheckSumFileSystem
LocalFileSystem uses ChecksumFileSystem to do its work, and this class makes it easy to add checksumming to other filesystems, as ChecksumFileSystem is just a wrapper around FileSystem.

~~~java

	FileSystem rawFs = ...
	FileSystem checksum = new CheckSumFileSystem(rawFs);

~~~

###Compression
There are many different compression formats, tools, and algorithms.

format | splittable | Codecs
--- | --- | ----
.deflate | No | DefualCodec
.gz | No | GzipCodec
.bz2 | Yes | Bzip2Codec
.lzo | No | LzoCodec
.lz4 | No| Lz4Codec
.snappy | No | SnappyCodec

- gzip is a general purpose compressor and sits in the middle of the space/time trade-off.
- bzip2 compresses more effectively than gzip but is slower.
- Lzo,Lz4 more fast but less effectively.

Splittable compression formats are especially suitable for MapReduce.

###Using Comresssion in Mapreduce
In order to compress the output of a Mapreduce job, in the job configuration ,set the *mapreduce.output.fileoutputformat.compress* property to ture and set *mapreduce.output.fileoutputformat.compress.codc* proterty to the classname of the compress code you want to use.

Alternatively, you can use FileOutputFormt to set these porperties.

~~~java
	
	Job job = new Job();
	FileOutputFormat.setCompressOutput(job,true);
	FileOutputFormat.setOutputCompressorClass(job,GizpCodec.class);

~~~

the mapreduc.out.put.fileoutputformat.compress.type property to control the type if compresion to use. the default is RECORD.

There is also a static convenience method on SequenceFileOutputFormat called setOutputCompressionType()


####Compressing map output

~~~java
	
	Configuration conf = new Configuration();
	conf.setBoolean(Job.MAP_OUTPUT_COMPRESS,true);
	conf.setClass(Job.MAP_OUTPUT_COMPRESS_CODEC,GzipCodec.class,CompressionCodec.class);
	Job job = new Job(conf);

	//or 
	conf.setCompressMapOutput(true);
	conf.setMapOutputCompressorClass(GizpCodec.class);
~~~

###Serialization
Serialization is the process of turning structured objects into a byte stream for transimission over network or writing to persistent storage.
Deserialization is the reverse process of turning a byte stream back into a series of structured objects.

Serialization is used in two quite distinct areas of distributed data processing:

1. interprocess communication
1. persistent storage

In Hadoop, interprocess communication between nodes in the system is implemented usring PRC.

The RPC protocl uses serialization to render the message into a binary stream to be sent to the remote node, which then deserialize the binary stream into the original mesage.

In general, it is desirable that RPC serialization format is:

- Compat
- Fast
- Extensible
- Interoperable

Hadoop uses its own serialization format, Writables, which is certainly compact and fast, but not so easy to extend or use from language other than Java.

### The Writable Interface

~~~java

	pubilc interface Writable{
		void write(DataOutput out) throw IOExcetion;
		void readFields(DataInput in) throw IOExcetion;
	}
~~~

Writable Classes

- wrappers for java primitives
	- BooleanWritable
	- ByteWritable
	- Short..
	- VInt..
	- Float..
	- Long..
	- VLong..
	- Double..
	

###Developing a MapReduce Application

####















