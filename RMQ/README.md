# Range Minimun Queries(Part One)

>本文参考自斯坦福大学数据结构课程 [CS166](http://web.stanford.edu/class/archive/cs/cs166/cs166.1166/) 的 [Range Minimum Queries, Part One](http://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/00/Slides00.pdf)

# 问题描述

**给定长度为 $n$ 的数组A，以及两个下标 $i,j(i\le j) $, 求出 $ A[i], A[i + 1], ... , A[j]$ 的最小值。**

乍一看问题并没有任何难度，直接枚举 $i,j$ 之间的元素，取出最小的即可，时间复杂度为$O(n)$。但假如存在很多组询问呢？

对于一个长度为 $n$ 的数组，最多存在 $1+2+3+...+n=n(n+1)/2$ 即 $O(n^2)$ 个合法询问，若采用上述解法:

* 询问个数：$O(n^2)$ 
* 每次询问花费的时间：$O(n)$
* 总时间复杂度：$O(n^3)$

下面将讨论一些优化算法，为了方便，记 $RMQ(i, j)$ 为区间 $[i, j]$ 的最小值；记某个 $RMQ$ 算法的时间复杂度为：$<p(n), q(n)>$ ，其中：

* $p(n)$ 表示预处理的时间复杂度
* $q(n)$ 表示查询的时间复杂度

那么可将上述枚举算法的时间复杂度则可记为：$<O(1), O(n)>$。

# 动态规划

可以采用动态规划在 $O(n^2)$ 的时间内预处理出所有的合法询问，之后便可以在 $O(1)$ 时间内查询，其时间复杂度记为：$<O(n^2), O(1)>$。

具体算法为：依次求出长度为 $1, 2,..., n$ 的所有区间的最小值，在求长度为 $k(1<k\le n)$的区间: $[i, j] (j-i+1=k)$ 时，可利用两个长度为 $k-1$ 的区间 $ [i, j-1] $ 和  $[i+1, j]$ 直接比较求出，其状态转移方程为：
$$
f[i][j]=min(f[i][j-1],f[i+1][j])
$$
状态初始化为：$f[i][i]=a[i](0\le i < n)$。

则预处理的时间复杂度如下：

* 长度个数：$O(n)$
* 每个长度的区间个数：$O(n)$
* 求解每个区间花费：$O(1)$
* 总时间复杂度：$O(n^2)$

预处理完之后，$f[i][j]$ 即为 $RMQ(i, j)$ 的值。

例如对于如下的数据：

|  $i$   |  0   |  1   |  2   |  3   |  4   |
| :----: | :--: | :--: | :--: | :--: | :--: |
| $A[i]$ |  3   |  2   |  4   |  1   |  5   |

其求解过程如下图所示：

{% asset_img dp_draw.gif %}

具体代码如下：

```python
from math import inf

class Dp(object):
    def __init__(self, a):
        self.n = len(a)
        self.a = a
        self.f = [[inf for _ in range(self.n)] for _ in range(self.n)]

    def preprocess(self):
        # Initialize the number in the diagonal.
        for i in range(self.n):
            self.f[i][i] = self.a[i]

        # Iterator the diagonals.
        # l means the index of the diagonal(start from 0).
        for l in range(1, self.n):
            for i in range(0, self.n - l):
                j = i + l
                self.f[i][j] = min(self.f[i][j - 1], self.f[i + 1][j])

    def rmq(self, i, j):
        return self.f[i][j]

if __name__ == '__main__':
    a = [3, 2, 4, 1, 5]
    dp = Dp(a)
    dp.preprocess()
    print(dp.rmq(1, 3))
```

# 分块

还可以采用分块的方法，将数组划分为连续的 $O(n/b)$ 个大小为 $b$ 的块，预处理出每一块的最小值，预处理的时间复杂度为：

* 块个数：$O(n/b)$
* 块大小：$O(b)$
* 总时间复杂度：$O(n)$

计算 $RMQ(i, j)$ 时，其过程及时间复杂度为：

* 找到 $i,j$ 所在块编号：$O(1)$
* 在 $i, j$ 所在的两块中枚举寻找最小值：$O(b)$
* 在 $i, j$ 之间的块间枚举寻找最小值：$O(n/b)$
* 总时间复杂度：$O(n/b+b)$，经求导计算得出 $b=\sqrt n$ 时取得最小值，即：$O(\sqrt n)$

其时间复杂度记为：$<O(n), O(\sqrt n)>$。

例如对于如下数据：

|  $i$   |  0   |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  10  |  11  |  12  |  13  |
| :----: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| $A[i]$ |  3   |  5   |  4   |  1   |  2   |  9   |  7   |  6   |  5   |  8   |  2   |  4   |  7   |  4   |

其求解 $RMQ(1, 13)$ 过程如下图所示：

{% asset_img block_draw.gif %}

具体代码如下：

```python
from math import sqrt, inf

class Block(object):
    def __init__(self, a):
        self.n = len(a)
        self.len_b = int(sqrt(self.n))
        self.cnt_b = (self.n - 1) // self.len_b + 1
        self.a = a
        self.f = [inf for _ in range(self.cnt_b)] 

    def preprocess(self):
        # Find the minium in every blocks.
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                # Maybe overflow.
                if j >= self.n:
                    break
                self.f[i] = min(self.f[i], self.a[j])

    def rmq(self, i, j):
        ans = inf
        
        # Calculate the index of block containing i/j.
        ith = i // self.len_b
        jth = j // self.len_b
        # iterator within the block to find the minium. 

        if ith == jth:
            for k in range(i, j + 1):
                ans = min(ans, self.a[k])
        else:
            for k in range(i, ith * self.len_b + self.len_b):
                ans = min(ans, self.a[k])
            for k in range(jth * self.len_b, j + 1):
                ans = min(ans, self.a[k])
            # Iterator the blocks between i and j to find the minium.
            for k in range(ith + 1, jth):
                ans = min(ans, self.f[k])
        return ans


if __name__ == '__main__':
    a = [3, 5, 4, 1, 2, 9, 7, 6, 5, 8, 2, 4, 7, 4]
    block = Block(a)
    block.preprocess()
    print(block.rmq(1, 13))
```

# 稀疏表

对于上文的动态规划算法，对所有 $O(n^2)$ 个区间进行了预处理，可以通过减少预处理的区间个数（在保证依旧可以 $O(1)$ 查询的前提下）来进行优化，具体方法为：对于每一个可能的区间起点 $i(0\le i < n)$ ，求出从 $i$ 开始的长度为 $2^0, 2^1, ..., 2^k$ （直到不能再大为止）的区间的最小值（即求出所有长度为2的幂的区间），其时间复杂度为：

* 可能的起点个数：$O(n)$
* 每个起点最多计算的区间个数：$O(log(n))$

* 求解每个区间最小值时的花费：$O(1)$
* 总时间复杂度：$O(nlog(n))$

预处理的难点在于如何求解每个区间最小值来使得其花费为 $O(1)$。可以利用上文的动态规划思想，具体算法为：依次求出长度为 $2^0, 2^1, ..., 2^k$ 的所有区间的最小值，在求长度为 $2^l(0<l\le k)$的区间: $[i, j] (j-i+1=2^l)$ 时，可利用两个长度为 $l-1$ 的区间 $ [i, i + 2^{l-1}-1] $ 和  $[i+2^{l-1}, j]$ 直接比较求出。为了节省状态空间，定义 $f[i][l]$ 为：起点为 $i$, 区间长度为 $2^l$ 的区间最小值，其状态转移方程为：
$$
f[i][l]=min(f[i][l-1], f[i+2^{l-1}][l-1])
$$
状态初始化为：$f[i][0]=a[i](0\le i< n)$。

计算 $RMQ(i, j)$ 时，其过程及时间复杂度为：

* 求出最大的 $k$ 使得 $2^k\le j-i+1$：$O(1)$

* 区间 $[i, j]$ 可分解为 $[i, i+2^k-1], [j-2^k+1, j]$ 的并集，取两区间最小值：$O(1)$
* 总时间复杂度：$O(1)$

对于区间的分解，作如下解释：因为预处理过程中只求出了所有长度为2的幂的区间，所以分解的两个区间的长度都要是2的幂，故第一个区间从 $i$ 开始，长度为 $2^k$，第二个区间需要覆盖剩余区间，故以 $j$ 为结尾，向前延伸到长度为 $2^k$ 为止，由于 $2^{k+1}>j-i+1$，故两区间必覆盖区间 $[i, j]$。

其时间复杂度记为：$<O(nlog(n)), O(1)>$。

例如对于如下数据：

|  $i$   |  0   |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |
| :----: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| $A[i]$ |  2   |  9   |  7   |  6   |  5   |  1   |  8   |  3   |  4   |  6   |

其预处理过程如下图所示：

{% asset_img st_draw.gif %}

其求解 $RMQ(2, 8)$ 时，过程如下：

* 求出 $k=log(8-2)=2$
* 将区间分解为：$[2, 2 + 2^2-1], [8-2^2+1, 8]$， 即：$[2,5],[5,8]$，其区间最小值为：$min(f[2][2], f[5][2])$

具体代码如下：

```python
from math import pow, log 

class St(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.f = [[0 for _ in range(self.n)] for _ in range(self.n)]

    def preprocess(self):
        for i in range(self.n):
            self.f[i][0] = self.a[i] 

        k = int(log(self.n) / log(2))
        for l in range(1, k + 1):
            for i in range(self.n):
                if i + int(pow(2, l)) - 1 >= self.n:
                    break
                self.f[i][l] = min(self.f[i][l - 1], self.f[i + int(pow(2, l - 1))][l - 1])

    def rmq(self, i, j):
        k = int(log(j - i + 1) / log(2))
        return min(self.f[i][k], self.f[j - int(pow(2, k)) + 1][k])

if __name__ == '__main__':
    a = [2, 9, 7, 6, 5, 1, 8, 3, 4, 6]
    st = St(a)
    st.preprocess()
    print(st.rmq(2, 8))
```

# 算法组合

现在，共有了四种求解 $RMQ$ 的算法：

* 不进行任何预处理：$<O(1), O(n)>$
* 预处理全部区间（动态规划）：$<O(n^2), O(1)>$
* 分块：$<O(n), O(\sqrt n)>$
* 预处理一部分区间（稀疏表）：$<O(nlog(n)), O(1)>$

可以通过如下方式进行算法组合：

* 将数组分成 $O(n/b)$ 个大小为 $b$ 的块
* 对于每一块求出最小值
* 以块为单位选择一种 $RMQ$ 算法
* 在每一块内部选择一种 $RMQ$ 算法
* 将两种 $RMQ$ 结构求出的结果进行比较求出最终结果

关键点在于如何：

* 选择合适的块大小 $b$
* 选择块间 $RMQ$ 算法
* 选择块内 $RMQ$ 算法

假设选择时间复杂度为 $<p_1(n), q_1(n)>$ 的块间 $RMQ$ 算法，时间复杂度为 $<p_2(n), q_2(n)>$ 的块内 $RMQ$ 算法，

则预处理的时间复杂度为：

* 计算出每一块内的最小值：$O(n)$
* 块间 $RMQ$ 算法：$p_1(n/b)$
* 在 $O(n/b)$ 块内进行 RMQ 算法：$O(n/b)p_2(b)$
* 总时间复杂度为：$O(n+p_1(n/b)+(n/b)p_2(b))$

查询的时间复杂度为：

* 块间查询：$q_1(n/b)$
* 块内查询：$q_2(b)$
* 总时间复杂度：$O(q_1(n/b)+q_2(b))$

## 组合1（稀疏表+无预处理）

块间采用稀疏表算法，块内不进行预处理，块大小为 $log(n)$，即：
$$
\begin{eqnarray*}
&p_1&(n)=nlog(n)\\\\
&q_1&(n)=1\\\\
&p_2&(n)=1\\\\
&q_2&(n)=n\\\\
&b&=log(n)
\end{eqnarray*}
$$
预处理的时间复杂度为：
$$
\begin{eqnarray*}
&O&(n+p_1(n/b)+(n/b)p_2(b))\\\\
=&O&(n+n/b\cdot log(n/b)+n/b)\\\\
=&O&(n+n/log(n)\cdot log(n/log(n))+(n/log(n)))\\\\
=&O&(n+n/log(n)\cdot log(n)+n)\\\\
=&O&(n)
\end{eqnarray*}
$$
查询的时间复杂度为：
$$
\begin{eqnarray*}
&O&(q_1(n/b)+q_2(b))\\\\
=&O&(1+log(n))\\\\
=&O&(log(n))
\end{eqnarray*}
$$
故其时间复杂度可记为：$<O(n), O(log(n))>$。

其代码如下：

```python
from math import sqrt, log, pow, inf
from st import St

class Combine1(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.len_b = max(1, int(log(self.n)/log(2)))
        self.cnt_b = (self.n - 1) // self.len_b + 1

    def preprocess(self):
        f = [inf for _ in range(self.cnt_b)] 
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                if j >= self.n:
                    break
                f[i] = min(f[i], self.a[j])

        self.st = St(f)
        self.st.preprocess()

    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b

        if ith == jth:
            for k in range(i, j + 1):
                ans = min(ans, self.a[k])
        else:
            for k in range(i, ith * self.len_b + self.len_b):
                ans = min(ans, self.a[k])
            for k in range(jth * self.len_b, j + 1):
                ans = min(ans, self.a[k])

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans
```





## 组合2（稀疏表+稀疏表）

块间与块内均采用稀疏表，块大小为 $log(n)$，即：
$$
\begin{eqnarray*}
&p_1&(n)=nlog(n)\\\\
&q_1&(n)=1\\\\
&p_2&(n)=nlog(n)\\\\
&q_2&(n)=1\\\\
&b&=log(n)
\end{eqnarray*}
$$
预处理的时间复杂度为：
$$
\begin{eqnarray*}
&O&(n+p_1(n/b)+(n/b)p_2(b))\\\\
=&O&(n+n/b\cdot log(n/b)+n/b\cdot b\cdot log(b))\\\\
=&O&(n+n/log(n)\cdot log(n/log(n))+n\cdot log(log(n)))\\\\
=&O&(n+n+n\cdot log(log(n)))\\\\
=&O&(n\cdot log(log(n)))
\end{eqnarray*}
$$
查询的时间复杂度为：
$$
\begin{eqnarray*}
&O&(q_1(n/b)+q_2(b))\\\\
=&O&(1)
\end{eqnarray*}
$$
故其时间复杂度可记为：$<O(n\cdot log(log(n))), O(1)>$。

其代码如下：

```python
from math import sqrt, log, pow, inf
from st import St

class Combine2(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.len_b = max(1, int(log(self.n)/log(2)))
        self.cnt_b = (self.n - 1) // self.len_b + 1

    def preprocess(self):
        f = [inf for _ in range(self.cnt_b)] 
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                if j >= self.n:
                    break
                f[i] = min(f[i], self.a[j])

        # ST between blocks.
        self.st = St(f)
        self.st.preprocess()

        # ST winth block.
        self.sts = []
        for i in range(self.cnt_b):
            tmp = self.a[i * self.len_b : min(self.n, i * self.len_b + self.len_b)]
            self.sts.append(St(tmp))
            self.sts[i].preprocess()

    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b

        i -= ith * self.len_b
        j -= jth * self.len_b
        if ith == jth:
            ans = min(ans, self.sts[ith].rmq(i, j))  
        else:
            ans = min(ans, self.sts[ith].rmq(i, self.len_b - 1))
            ans = min(ans, self.sts[jth].rmq(0, j))

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans
```



## 组合3（稀疏表+组合1）

块间采用稀疏表算法，块内采用组合1算法，块大小为 $log(n)$，即：
$$
\begin{eqnarray*}
&p_1&(n)=nlog(n)\\\\
&q_1&(n)=1\\\\
&p_2&(n)=n\\\\
&q_2&(n)=log(n)\\\\
&b&=log(n)
\end{eqnarray*}
$$
预处理的时间复杂度为：
$$
\begin{eqnarray*}
&O&(n+p_1(n/b)+(n/b)p_2(b))\\\\
=&O&(n+n/b\cdot log(n/b)+n/b\cdot b)\\\\
=&O&(n+n/log(n)\cdot log(n/log(n))+n)\\\\
=&O&(n)
\end{eqnarray*}
$$
查询的时间复杂度为：
$$
\begin{eqnarray*}
&O&(q_1(n/b)+q_2(b))\\\\
=&O&(1+log(log(n)))\\\\
=&O&(log(log(n)))
\end{eqnarray*}
$$
故其时间复杂度可记为：$<O(n), O(log(log(n)))>$。

其代码如下：

```python
from math import sqrt, log, pow, inf
from st import St
from combine1 import combine1

class Combine3(object):
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.len_b = max(1, int(log(self.n)/log(2)))
        self.cnt_b = (self.n - 1) // self.len_b + 1

    def preprocess(self):
        f = [inf for _ in range(self.cnt_b)] 
        for i in range(self.cnt_b):
            for j in range(i * self.len_b, i * self.len_b + self.len_b):
                if j >= self.n:
                    break
                f[i] = min(f[i], self.a[j])

        # ST between blocks.
        self.st = St(f)
        self.st.preprocess()

        # ST winth block.
        self.combine1s = []
        for i in range(self.cnt_b):
            tmp = self.a[i * self.len_b : min(self.n, i * self.len_b + self.len_b)]
            self.combine1s.append(Combine1(tmp))
            self.combine1s[i].preprocess()

    def rmq(self, i, j):
        ans = inf
        ith = i // self.len_b 
        jth = j // self.len_b

        i -= ith * self.len_b
        j -= jth * self.len_b
        if ith == jth:
            ans = min(ans, self.combine1s[ith].rmq(i, j))  
        else:
            ans = min(ans, self.combine1s[ith].rmq(i, self.len_b - 1))
            ans = min(ans, self.combine1s[jth].rmq(0, j))

        if ith + 1 <= jth - 1:
            ans = min(ans, self.st.rmq(ith + 1, jth - 1))
        return ans
```



# 总结

至此，共得出7种算法，如下：

* 不进行任何预处理：$<O(1), O(n)>$
* 预处理全部区间（动态规划）：$<O(n^2), O(1)>$
* 分块：$<O(n), O(\sqrt n)>$
* 预处理一部分区间（稀疏表）：$<O(nlog(n)), O(1)>$
* 组合1：$<O(n), O(log(n))>$
* 组合2：$<O(n\cdot log(log(n))), O(1)>$
* 组合3：$<O(n), O(log(log(n)))>$

另外，稀疏表再此和组合2组合，可以继续减少预处理的时间复杂度为 $O(n\cdot log(log(log(n)))$，查询时间复杂度不变；稀疏表再此和组合3组合，可以继续减少查询的时间复杂度为 $O(log(log(log(n)))$，预处理时间复杂度不变。组合可以一直进行下去。

**点击[下载]()所有代码。**

