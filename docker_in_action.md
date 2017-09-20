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














