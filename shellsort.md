[TOC]
## ShellSort

It is also called **disminishing increment**. ShellSort makes comparisions and swaps between non-adjacent elements. ShellSort *exploits* the best-casse performence of Insertion Sort. ShellSort's stratege is to make the list "mostly sorted" so that a final Insertion Sort can finish the job.

ShellSorts uses a process that forms the basis for many of the sorts presented in the following sections:

- Break the list into sublists
- sort them
- recombine the sublist

shellsorts breaks the array of elements into "Virtual" sublists. Each sublist is sorted using insertion sort. Another group of sublists is then chosen and sorted, and so on.

### code

```java

	public static <E extends Comparable<? super E> void Sort(E[] A){
		for(int i=A.length/2; i>2; i/=2) // for each increment
			for(int j=0; j<i; j++) // sort each sublist
				insertsort(A,j,i);
		insertsort(A,0,1);			
	} 

	pubblic static<E extends Comparable<? super E> void insertsort(E[] A,int start,int incr){
		for(int i=start+incr;i<A.length;i+=incr){
			for(int j=i; (j>=incr)&&(A[j].compareTo(A[j-incr])<0); j-=incr)
				DSutil.swap(A,j,j-incr);
		}
	}

```

> A better choice of increments is the follow series based on division by three:
(....,121,40,13,4,1).


> ShellSort illustrates how we can sometiems exploit the special properties of an algorithm even if in general the algorithm is unacceptable slow.

