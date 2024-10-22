import psutil

def bytes2human(n):
    symbols = (' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB')
    prefix = {}
    for i, s in enumerate(symbols):
        # print(f"{i}:{s}")
        prefix[s] = 1 << (i + 1) * 10
        # print(prefix)
    for s in reversed(symbols):
        if abs(n) >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f%s' % (value, s)
    return "%sB" % n
# print(bytes2human(6000024))

def ram():
    total_ram = psutil.virtual_memory()
    return 'RAM: ' + str( bytes2human(total_ram.total))
# print(ram())

def ram_used():
    ram_used = psutil.virtual_memory()
    return float(bytes2human(ram_used.used).strip("GB"))
# print(ram_used())

def ram_percent():
    percent = psutil.virtual_memory().percent
    return percent
# print(ram_percent())


