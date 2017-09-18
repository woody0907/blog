[TOC]
## <I></I>nsertion Sort
Insertion sort iterates through a list of records. Each record is inserted in turn at the correct position within a sorted list composted of those records already processed.

###code

```java


public static <AnyType extends Comparable<? super AnyType>>
    void insertSort2(AnyType[] a){
        for(int i = 1;i<a.length;i++){
            for(int j = i; j>0 && a[j].compareTo(a[j-1])<0;j--){
                swapReferences(a,j-1,j);
            }
        }
    }

public static <AnyType extends Comparable<? super AnyType>>
    void insertSort1(AnyType[] a){
        int j;
        for (int i = 1; i < a.length; i++) {
           AnyType temp = a[i];
            for ( j = i; j >0 && temp.compareTo(a[j-1])<0; j--) {
                a[j] = a[j-1];
            }
            a[j]=temp;
        }
    }

```