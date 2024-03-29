Library(ggplot2)
set.seed(1234)
x <- rnorm(100,mean = 2, sd = 3)
y <- -1.5 + 2*x + rnorm(100)
df <- data.frame(x = x, y = y)
ggplot(data = df, mapping = aes(x = x, y = y)) + geom_point()
