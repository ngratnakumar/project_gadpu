#docker run -it -h gadpu -v /data/:/data ngratnakumar/gadpu_spam_01oct2018 /bin/bash -c "/data/CYCLE22/start_docker.sh sayalitest/ 11 "
#su -c "/data/CYCLE22/initialize.sh $1 $2" - gadpu

docker run -it -h gadpu -v /data/:/data ngratnakumar/gadpu_spam_01oct2018 /bin/bash -c "su -c \"/data/CYCLE22/initialize.sh $1 $2\" - gadpu"

#echo "hi \" $1 $2\""
