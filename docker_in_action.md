rename container
    
    docker rename webid webid-old

the docker create is similar to docker run, the primary difference being that the container is created in a stopped state:

    docker create nginx

get the truncated ID of the last create container:

    CID = $(docker ps --latest --quiet)
    CID = $(docker ps -l -q)

to see all the containers

    docker ps -a

###Building environment-agnostic system
* Read-only file systems
* Environment variable injection
* Volumes

####Read-only file system:
    
    docker run -d --name wp --read-only wordpress:4

docker inspect command will display all the metadata that docker maintains for the container

    docker inspect --format "{{.State.Running}}" wp


run mysql

     docker run -d --name wpdb \
    -e MYSQL_ROOT_PASSWORD=ch2demo \
    mysql:5

run wordpress linked with mysql

    docker run -d --name wp2 \
    --link wpdb:mysql \
    -p 80 --read-only \
    wordpress:4

    # Start the container with specific volumes for read only exceptions
    docker run -d --name wp3 --link wpdb:mysql -p 80 \
    -v /run/lock/apache2/ \
    -v /run/apache2/ \
    --read-only wordpress:4

####Environment variable injection
the unit commmon __env__ display all the environment varibles in the current exection context

    docker run --evn[or -e] MY_ENVIRONMENT_VARIBLE = "this is a test" busybox:latest \
    env

    docker create \
    --env WORDPRESS_DB_HOST=<my database hostname> \
    --env WORDPRESS_DB_USER=site_admin \
    --env WORDPRESS_DB_PASSWORD=MeowMix42 \
    wordpress:4

###Building durable containers

Docker contains can be in one of the four states:

+ Running
* Paused
* Restarting
* Exited

####Automatically restarting container
--restart tell the container to the following

* Never restart(default)
* Attempt to restart when a failure is detected
* Attempt for a predetermined time to restart when a failure is detected
* Always restart regardless of the condition

####Keeping containers running with supervisor and precesses

    docker run -d -p 80:80 --name lamp-test tutum/lamp

you can see what processes are running inside this container by using

    docker top lamp-test

kill a process inside a container
    
    docker exec lamp-test ps
    docker exec lamp-test kill <PID>

###Identifying software

repository and tag

###Find and installing software

    docker login
    docker logout
    docker search
    docker pull

    https://hub.docker.com

    [REGISTRYHOST/][USERNAME/]NAME[:TAG]

####Images as files

    

    #save image to file 
    docker pull busybox:latest
    docker save -o myfile.tar busybox:latest
    #if the image is exits the remove it 
    docker rmi busybox

    docker load -i myfile.tar

####Install from a Dockerfile
A Dockerfile is a script that descript steps for dockers to take to build a new image.

    git clone https://github.com/dockerinaction/ch3_dockerfile.git
    docker build -t dia_ch3/dockerfile:latest ch3_dockerfile    

###Installation files and isolation
####Image layers

union file 
MNT
chroot

####Bind mount volume

    docker run --name bmweb_ro \
    --volume ~/example-docs:/usr/local/apache2/htdocs/:ro \  #-ro means readonly
    -p 80:80 \
    httpd:latest
if you specify a host directory that doesn't exits, docker will create it for you.
bind mount volume aren't limited to directories.(the important thing is to note is that the file must exist on the host before you create the container)



####Docker-managered volume
Docker daemon creates managee volumes in a portion of host's file system that's owned by Docker

    docker run -d \
    -v /var/lib/cassandra/data \ #only specify the mount point in the container
    --name cass-shared \
    alpine echo Data Container

    #to find out where this file is (Managee Volumes are created on the machine that's running the docker daemon)
    docker inspect -f "{{json .Volumes}}" cass-shared 

###Share Volumes

####Host-dependent share

    mkdir ~/web-logs-example

    docker run --name plath -d -v ~/web-logs-example:/data dockerinaction/ch4_writer_a

    docker run --rm  -v ~/web-logs-example:/reader-data alpine:latest head /reader-data/logA

    cat ~/web-logs-example/logA

    docker stop plath

####Generalized sharing

    docker run --name reader \
    --volumes-from fowler \
    --volumes-from knuth \
    alpine:latest ls -l /library/

###Volume life cycle

####Clean up volumes

attempt to delete any managed voluems referenced by the target container, any managed volumes that are referenced by other container will be skipped

    docker rm -v xxx

when you failed to last step, you'll make that volume an orphan. Removing orphaned volumes requires messy manual steps,there is a scipt to use.

remove all stopped containers and their volumes with the following command:

    docker rm -v $(docker ps -aq)

####data-packed volume containers

running and defining the volume and running a cp command at container-creation time

    docker run --name dpvc \
    -v /config \
    dockerinaction/ch4_packed /bin/sh -c 'cp /packed/* /config/'
    docker run --rm --volumes-from dpvc \
    alpine:latest ls /config
    docker run --rm --volumes-from dpvc \
    alpine:latest cat /config/packedData
    docker rm -v dpvc

####polymorphic container pattern

a polymorphic container is one that provides some functionality that's easily substitued using volumes

##Network Exposure

###four network container archetype
* Closed container
* Bridged container
* joined container
* open container

you can tell docker to creat a closed container by specifying none with the --net flag:
    
    docker run --net none alpine:latest \
    ip addr ##list the interface

docker create bridged container by default

    docker run --net bridege ....

####Custom name resolution

Docker provides different options for customizing the DNS configuration for a new container

First the docker run commannd has a --hostname flag:

    docker run --rm\
    --hostname barker \
    alphine:latest \
    nslookup barker ##resolve the host name to an IP address

the second option is to specify one or more DNS server to use.

    docker run --rm \
    --dns 8.8.8.8 \
    alpine:latest \
    nsloopup docker.com

the third dns related option, --dns-search

    docker run --rm \
    --dns-search docker.com \
    busybox:latest \
    nslookup registry.hub  ##look up shortcut for registry.hub.docker.com

the last DNS feature to consider provides the ability to override the DNS system

    docker run --rm \
    --add-host test:10.10.10.255 \
    alpine:latest \
    nslookup test

####Openning inbound communication

there is no way to get to a container from outside the host. Luckly,the docker run command provides  a flag -p or --publish, that you can use to creat a mapping between ports on the host's network stack and the new container's interface

    
    <containerPort>
    docker run -p 3333 ...
    <hostPort>:<containerPort>
    docker run -p 3333:3333 ...
    <ip>::<containerPort>
    docker run -p 192.168.0.32::2222 ...
    <ip>:<hostPort>:<containerPort>
    docker run -p 192.168.0.32:1111:1111 ...

if you can accept a dynamic or ephemeral port assignment on the host, you can use the -P or --publish-all flag.

--expose takes a port number that the container should expose, this flag can set multiple time.

    docker run -d --name philbin \
    --expose 8000 \
    -P \
    dockerinaction/ch5_expose

you can see what these ports were mapped to use:
    
    docker ps
    docker inspect
    docker port

you can configure it to diswallow network connections between containers.

    docker -d --icc=false

####modify the bridge interface

* define the address and subnet of the bridge
* define the range of IP address that can be assigned to containers
* define the maximum transmission unit(MTU)

```
    docker -d --bip "192.168.0.128" ...
```

with a network define for the bridge, you can go on to customize which ip addresses in that network can be assiged to new container

    docker -d --fixed-cidr "192.168.0.128/26"

you can use th --mtu flag to set the size in bytes:

    docker -d -mtu 1200

####open container
this type of container is created when you specify host as the value of --net option on docker run command:
    
    docker run --net host ...
















