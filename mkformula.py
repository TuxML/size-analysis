def _quote_size(s):
    return "`" + s + "`"

csizes = ['LZ4', 'BZIP2', 'GZIP', 'XZ', 'LZO', 'LZMA']

negated_variables = '-'.join([_quote_size(c) + "-" + _quote_size(c + "-bzImage") + "-" + _quote_size(c + "-vmlinux") for c in csizes])
formula = 'm1 <- rpart(vmlinux~.-' + negated_variables +', data=df_train, method  = "anova")'
print(formula)
