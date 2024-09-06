# ARL_Export



### 从数据库中导出站点信息



1、导出灯塔 站点 内容

```
docker exec -it arl /bin/bash -c 'mongo arl --eval "printjson(db.site.find().toArray())" > /tmp/output.json'
```

2、复制文件到本地

```
docker cp arl:/tmp/output.json output.json
```

3、清空全局查看的站点内容

```
docker exec -it arl /bin/bash -c 'mongo arl --eval "db.site.remove({})"'
```

4、使用脚本生成 csv

```
python ARL_Export.py
```



