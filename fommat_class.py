data = {'id': None, 'vulName': 'Siemens Solid Edge 安全漏洞', 'cnnvdCode': 'CNNVD-202302-1495',
        'cveCode': 'CVE-2023-23579', 'publishTime': '2023-02-17 00:00:00', 'isOfficial': 1, 'vendor': None,
        'hazardLevel': None, 'vulType': '其他', 'vulTypeName': '其他',
        'vulDesc': 'Siemens Solid Edge是德国西门子（Siemens）公司的一款三维CAD软件。该软件可用于零件设计、装配设计、钣金设计、焊接设计等行业。\r\nSiemens Solid Edge SE2022和Solid Edge SE2023存在安全漏洞，该漏洞源于在解析特制SLDPRT文件时存在超出分配缓冲区末尾的越界写入，攻击者利用该漏洞可以在当前进程的上下文中执行代码。',
        'affectedProduct': None, 'affectedVendor': None, 'productDesc': None, 'affectedSystem': None,
        'referUrl': '来源:www.auscert.org.au\r\n链接:https://www.auscert.org.au/bulletins/ESB-2023.0960',
        'patchId': None, 'patch': 'https://solidedge.siemens.com/zh-hans/', 'deleted': None, 'version': None,
        'createUid': None, 'createUname': None, 'createTime': None, 'updateUid': None, 'updateUname': None,
        'updateTime': '2023-02-17 00:00:00',
        'cnnvdFiledShow': 'vul_name,cnnvd_code,_code,publish_time,is_official,vendor,hazard_level,vul_type,vul_desc,affected_product,affected_vendor,product_desc,affected_system,refer_url,patch_id,product,update_time,patch',
        'cveVulVO': None, 'cveFiledShow': None, 'ibmVulVO': None, 'ibmFiledShow': None, 'icsCertVulVO': None,
        'icsCertFiledShow': None, 'microsoftVulVO': None, 'microsoftFiledShow': None, 'huaweiVulVO': None,
        'huaweiFiledShow': None, 'nvdVulVO': None, 'nvdFiledShow': None, 'varchar1': '其他'}
for key in data:
    value = data[key]
    name = key
    p = "String"
    if type(value) == int:
        p = "int"
    if value is None:
        value = ""
    print("private " + p + " " + str(key) + ";")
    print()

