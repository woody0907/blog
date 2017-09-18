[TOC]
## Mergesort

The natural approach to prolem solving is divide and conquer. In terms of sorting, we might consider breaking the list to be sorted into pieces, process the pieces, and put them back together somehow. 

### pseudocode

```
	List mergesort(List inlist){
		if(inlist.length()<=1) return inlist;;
		List l1 = half of the items from inlist;
		List l2 = other half of the items from inlist;
		return merge(mergesort(l1),mergesort(l2));
	} 

```		

> Mergesort is the method of choice when the input is in the form of a linked list, because mergesort does't require random access to the list elements.

### implementation

```java

    private static <AnyType extends Comparable<? super AnyType>>
    void mergeSort1(AnyType[] a, AnyType[] temp, int l, int r) {
        int mid = (l+r)/2;
        if(l==r) return;
        mergeSort1(a,temp,l,mid);
        mergeSort1(a,temp,mid+1,r);
        //auxiliary array
        for (int i = l; i <= r; i++) {
           temp[i] = a[i];
        }

        int i1 = l;
        int i2 = mid+1;

        for(int curr = l;curr<=r;curr++){
            if(i1==mid+1){ //Left sublist exhausted
                a[curr] = temp[i2++];
            }
            else if(i2>r){ //Left sublist exhausted
                a[curr] = temp[i1++];
            }
            else if(temp[i1].compareTo(temp[i2])<0){
                a[curr] =temp[i1++];
            }else{
                a[curr] = temp[i2++];
            }
        }


    }

```

> There is another implementation. It reverse the order of second subarray during the initial copy. Now the current positions of the two subarray works inwards from the ends, allowing the end of each subarray act as a sentinel for the other. Unlike the previous implementation, no test is needed to check for when one of the two subarrays becomes empty. 

```java

	static <E extends Comparable<? super E>>
	void mergesort(E[] A, E[] temp, int l, int r) {
	int i, j, k, mid = (l+r)/2; // Select the midpoint
	if (l == r) return; // List has one element
	if ((mid-l) >= THRESHOLD) mergesort(A, temp, l, mid);
	else inssort(A, l, mid-l+1);
	if ((r-mid) > THRESHOLD) mergesort(A, temp, mid+1, r);
	else inssort(A, mid+1, r-mid);
	// Do the merge operation. First, copy 2 halves to temp.
	for (i=l; i<=mid; i++) temp[i] = A[i];
	for (j=1; j<=r-mid; j++) temp[r-j+1] = A[j+mid];
	// Merge sublists back to array
	for (i=l,j=r,k=l; k<=r; k++)
	if (temp[i].compareTo(temp[j])<0) A[k] = temp[i++];
	else A[k] = temp[j--];
	}

```

