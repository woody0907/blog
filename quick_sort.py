
def quick_sort(a,i,j):
	pivort = find_pivort(a,i,j)
	swap(a,pivort,j)
	k = partition(a,i-1,j,a[j])
	swap(a,k,j)
	if(k-i>1):
		quick_sort(a,i,k-1)
	if(j-k>1):
		quick_sort(a,k+1,j)

def find_pivort(a,i,j):
	return j;

def swap(a,i,j):
	print(i)
	print(j)
	tmp = a[i]
	a[i] = a[j]
	a[j] = tmp

def partition(a,l,r,v):
	while (l<r):
		while (a[++l]<v):
			continue
		while (a[--r]>v and r!=0):
			continue
		swap(a,l,r)
	return l

def test():
	a = [10,9,8,7,6]
	quick_sort(a,0,len(a))
	print(a)
				
test()