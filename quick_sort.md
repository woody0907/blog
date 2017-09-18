### QuickSort

>While Mergesort use the most obvious form of divide and conquer, it is not the only way we can break down the sorting problem. And we saw that doing the merge set for Mergesort when using an array implementation is not so easy. So perhaps a different divide and conquer stratege might turn out to be more efficient?

>QuickSort is aptly named because, when properly implemented, it is the fastest known general-purpose in-memeory sorting algorithm in the average case. It does not require the extra array needed by mergesort, so it is space efficent as well.

>QuickSort first selects a value called the pivot. Assume that the input array contains k values less than the pivot. The record are then rearranged in such a way that the k values less than the pivot are placed in the first, or leftmost, k positions in the array, and the values greater than or equal to the pivot are placed in the last, or rightmost, n-k position. This is called partition of the array. The values placed in a given position need not be sorted with respect to each other. All that is required is that all values are end up in the correct position. The pivot values itself is placed in position k.


### Implementation

```java

	 public static <AnyType extends Comparable<? super AnyType>> void
    qsort(AnyType[] a, int i, int j) {
        int pivot = findPivot(a, i, j);//find pivot index
        swapReferences(a, pivot, j);//stic pivot at end
        int k = partition(a, i - 1, j, a[j]);// k will be the first postion in the right subarray
        swapReferences(a, k, j); //put pivot in place
        if ((k - i) > 1) qsort(a, i, k - 1);//sort left partition
        if ((j - k) > 1) qsort(a, k + 1, j);//sort right partition

    }
```

> Function partition will move record to the appropriate partition and return k, the first position in the right partition. Note that the pivot value is initially placed at the end of array. Thus, partition must not affect the value of array position j. After partition the pivot value is placed in position k, which is its correct position in the final, sorted array. By doing so, we guarantee that at least one value(the pivot) will not be processed in the recursive calls to qsort. 

```java
	
	  public static <AnyType extends Comparable<? super AnyType>> int
    partition(AnyType[] a, int l, int r, AnyType pivot) {
        do {
            while (a[++l].compareTo(pivot) < 0) ;
            while (a[--r].compareTo(pivot) > 0 && r != 0) ;
            swapReferences(a, l, r);
        } while (l < r);
        swapReferences(a, l, r);
        return l;
    }
```

