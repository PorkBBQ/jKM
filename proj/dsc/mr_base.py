#!/home/biadmin/anaconda/bin/python
import sys

intermediate =[]

def main():
    env='local' if len(sys.argv)==1 else 'mr'
    localFile=r'D:\Josh\data\DSC01\heckle\web.log.2'

    if env=='local':
        mapper('local', localFile)
        reducer('local')
    elif env=='mr':
        if sys.argv[1]=='-m':
            mapper('mr')
        elif sys.argv[1]=='-r':
            reducer('mr')


def mapOut(env, line):
    if env=='local':
        intermediate.append(line)
    elif env=='mr':
        print(line)

def mapper(env, localFile=''):
    if env=='local':
        datafile = open(localFile)
        it=datafile.readlines()
    elif env=='mr':
        it=sys.stdin
#------------------------------------------    
    for line in it:
        line = line.strip()
        mapOut(env, line)
#------------------------------------------

def reducer(env='local'):    
    if env=='local':
        it=intermediate 
    elif env=='mr':
        it=sys.stdin
        
#------------------------------------------    
    for line in it:
        line = line.strip()
        print(line)
#------------------------------------------    

if __name__ == '__main__':
    main()


'''
hadoop fs -rmr /tmp/dsc01_02a

hadoop jar $HADOOP_HOME/hadoop-streaming.jar \
-D mapred.job.name='dsc01_01a' \
-input /data/dsc01/heckle \
-input /data/dsc01/jeckle \
-output /tmp/dsc01_02a \
-file /home/biadmin/josh/script/dsc01/dsc01_02a.py \
-mapper "/home/biadmin/josh/script/dsc01/dsc01_02a.py -m" \
-reducer "/home/biadmin/josh/script/dsc01/dsc01_02a.py -r"

'''
