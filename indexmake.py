import os
from datetime import datetime

# 설정: 제외할 파일명 또는 폴더
EXCLUDE_FILES = ['index.html', 'generate_index.py', '.DS_Store']
EXCLUDE_DIRS = ['.git', '.github', '__pycache__']

def create_index_html():
    # 현재 디렉토리의 HTML 파일 목록 스캔
    html_files = []
    for root, dirs, files in os.walk("."):
        # 제외할 폴더 건너뛰기
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith(".html") and file not in EXCLUDE_FILES:
                # 상대 경로 계산 (하위 폴더 지원)
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, ".")
                # 윈도우 경로(\)를 웹 표준(/)으로 변환
                web_path = relative_path.replace(os.sep, '/')
                
                html_files.append({
                    'path': web_path,
                    'name': file,
                    'mtime': os.path.getmtime(full_path)
                })

    # 최신 수정일 순으로 정렬
    html_files.sort(key=lambda x: x['mtime'], reverse=True)

    # HTML 템플릿 작성
    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>강의 자료 목록</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans KR', sans-serif; background-color: #f7fafc; color: #2d3748; margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center; }}
        .container {{ width: 100%; max-width: 800px; }}
        header {{ margin-bottom: 40px; text-align: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; }}
        h1 {{ color: #0078D4; margin: 0; }}
        .file-list {{ list-style: none; padding: 0; }}
        .file-item {{ background: white; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 15px; transition: transform 0.2s, box-shadow 0.2s; }}
        .file-item:hover {{ transform: translateY(-3px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-color: #0078D4; }}
        .file-link {{ display: flex; align-items: center; padding: 20px; text-decoration: none; color: inherit; }}
        .icon {{ font-size: 24px; color: #0078D4; margin-right: 20px; width: 40px; text-align: center; }}
        .info {{ flex-grow: 1; }}
        .title {{ font-weight: 700; font-size: 18px; display: block; }}
        .meta {{ font-size: 14px; color: #718096; margin-top: 4px; }}
        .arrow {{ color: #cbd5e0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fa-solid fa-folder-open"></i> 강의 자료 아카이브</h1>
            <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </header>
        <ul class="file-list">
    """

    for file in html_files:
        mod_time = datetime.fromtimestamp(file['mtime']).strftime('%Y-%m-%d %H:%M')
        html_content += f"""
            <li class="file-item">
                <a href="{file['path']}" class="file-link" target="_blank">
                    <div class="icon"><i class="fa-brands fa-html5"></i></div>
                    <div class="info">
                        <span class="title">{file['name']}</span>
                        <span class="meta">수정일: {mod_time}</span>
                    </div>
                    <div class="arrow"><i class="fa-solid fa-chevron-right"></i></div>
                </a>
            </li>
        """

    html_content += """
        </ul>
    </div>
</body>
</html>
    """

    # index.html 파일 쓰기
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"성공: {len(html_files)}개의 파일을 포함한 index.html이 생성되었습니다.")

if __name__ == "__main__":
    create_index_html()
