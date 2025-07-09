import xml.etree.ElementTree as ET


def parse_nmap_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    hosts_data = []

    for host in root.findall('host'):
        ip_elem = host.find('address[@addrtype="ipv4"]')
        if ip_elem is None:
            continue
        ip = ip_elem.attrib['addr']

        for port in host.findall(".//port"):
            port_id = port.attrib.get('portid', 'unknown')
            protocol = port.attrib.get('protocol', 'unknown')
            state_elem = port.find('state')
            state = state_elem.attrib.get('state') if state_elem is not None else 'unknown'

            service_elem = port.find('service')
            service = service_elem.attrib.get('name', 'N/A') if service_elem is not None else 'N/A'

            hosts_data.append({
                'ip': ip,
                'port': port_id,
                'protocol': protocol,
                'state': state,
                'service': service
            })

    return hosts_data


def generate_html_report(parsed_data, output_file='htmlrapor.html'):
    with open(output_file, 'w') as f:
        f.write("""<html>
<head><title>Nmap Raporu</title></head>
<body>
<img src="logo.png" alt="Logo" height="100"><br>
<h2>Nmap Port Raporu</h2>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>IP</th><th>Port</th><th>Protocol</th><th>Durum</th><th>Servis</th></tr>
""")
        for entry in parsed_data:
            f.write(
                f"<tr><td>{entry['ip']}</td><td>{entry['port']}</td><td>{entry['protocol']}</td><td>{entry['state']}</td><td>{entry['service']}</td></tr>\n")

        f.write("</table></body></html>")


if __name__ == "__main__":
    nmap_xml_path = "scan.xml"
    parsed_data = parse_nmap_xml(nmap_xml_path)
    generate_html_report(parsed_data)
    print("HTML raporu oluştu: report.html")
