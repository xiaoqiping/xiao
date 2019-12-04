try:
    callMod = __import__(modul)  # 根据module名，反射出module
    pc_dict[modul] = callMod  # 预编译字典缓存此模块
except Exception as e:
    print('模块不存在:%s' % modul)
    self._socket.sendall(("F" + "module '%s' is not exist!" % modul).encode(php_python.CHARSET))  # 异常
    self._socket.close()
    return