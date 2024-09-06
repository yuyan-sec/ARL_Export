import json
import re
import csv
import argparse

# 读取并处理 JSON 数据，跳过前面指定的行
def process_json_from_file(input_file, num_lines_to_skip, csv_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        # 跳过指定的前几行
        for _ in range(num_lines_to_skip):
            next(file)
        
        # 读取剩余的 JSON 数据
        content = file.read()
        cleaned_content = re.sub(r'ObjectId\("([0-9a-fA-F]{24})"\)', r'"\1"', content)
        try:
            data = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            print(f"JSON 解码错误: {e}")
            return
    
    # 保存到 CSV 文件
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['site', 'hostname', 'ip', 'title', 'status', 'http_server', 'finger_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入 CSV 头部
        writer.writeheader()

        # 写入数据
        for doc in data:
            site = doc.get('site')
            hostname = doc.get('hostname')
            ip = doc.get('ip')
            title = doc.get('title')
            status = doc.get('status')
            http_server = doc.get('http_server')
            
            # 提取 finger 的 name 值
            finger_names = [finger.get('name', '') for finger in doc.get('finger', [])]
            finger_names_str = '; '.join(finger_names)  # 将多个 name 用分号分隔
            
            writer.writerow({
                'site': site,
                'hostname': hostname,
                'ip': ip,
                'title': title,
                'status': status,
                'http_server': http_server,
                'finger_name': finger_names_str
            })
    
    print(f"数据已保存为 {csv_file}")

# 主函数
def main():
    parser = argparse.ArgumentParser(description="Process JSON data and save to CSV.")
    parser.add_argument('-i', '--input_file', type=str, default='output.json', help='Input JSON file path (default: output.json)')
    parser.add_argument('-o', '--csv_file', type=str, default='output.csv', help='Output CSV file path (default: output.csv)')
    parser.add_argument('-n','--skip-lines', type=int, default=4, help='Number of lines to skip at the beginning of the JSON file (default: 4)')

    args = parser.parse_args()
    
    process_json_from_file(args.input_file, args.skip_lines, args.csv_file)

if __name__ == "__main__":
    main()
