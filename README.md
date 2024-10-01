# read-write lock manager

## Assignement:
[First Phase](https://github.com/nunoinfante/AD/tree/master/projeto_1)  
[Second Phase](https://github.com/nunoinfante/AD/tree/master/projeto_2)

## About:
The overall aim of the project was to create a resource lock manager for reading and writing. Its purpose is to control access to a set of resources in a distributed system, where different clients can request access concurrently. The project was developed in two phases:
- The first one focused on creating commands that are exchanged between the client and the server such as LOCK, UNLOCK, STATUS, STATS and PRINT. It was also needed to represent the state of the resourses using UNLOCKED, LOCKED-R (for reading) and LOCKED-W (for writing). As the server received the commands sent by the client, it implements methods to process the commands. 
* The second focused on modificating the first phase of the project. Modifications include the implementation of serialized communication, where messages between the client and server are now sent as Python lists instead of strings. The programs client and server were reorganized using a communication model based on RPC. At last, it now supports multiple clients with established connections to the server
