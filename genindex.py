import os
import markdown
from datetime import datetime

def generate_index():
    # 제외할 폴더 및 파일 설정
    exclude_dirs = {'.git', '.github', '.pytest_cache', '__pycache__', 'assets'}
    exclude_files = {'index.html', 'generate_index.py', 'genindex.py', 'README.md'}
    
    # 디자인 테마 변경: 해킹 및 클라우드 보안 분위기의 어두운 테마 적용
    html_header = f"""<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security & Cloud Hacking Lab</title>
    <!-- Tailwind CSS 및 Typography 플러그인 로드 -->
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <!-- Font Awesome 아이콘 로드 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Web Fonts (Noto Sans KR) 로드 -->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        
        /* 기본 글꼴 및 다크 모드 배경색 설정 */
        body {{ 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: #020617; /* 매우 어두운 남색 배경 */
            color: #e2e8f0; /* 밝은 회색 텍스트 */
            /* 전체 화면 배경 이미지 적용 및 투명도(Overlay) 설정: 사진이 잘 보이도록 투명도 낮춤 */
            background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.4), rgba(2, 6, 23, 0.75)), 
                              url('image_1a3201.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center center;
        }}

        /* 텍스트 리스트 호버 효과: 터미널 스타일 */
        .list-hover {{
            transition: all 0.2s ease;
        }}
        .list-hover:hover {{
            color: #22d3ee; /* 호버 시 사이안(Cyan) 색상 강조 */
            padding-left: 0.5rem; /* 호버 시 살짝 우측으로 이동 */
            background-color: rgba(15, 23, 42, 0.6); /* 어두운 반투명 배경 */
        }}
    </style>
    <!-- Tailwind 설정 커스터마이징 (다크 모드 활성화) -->
    <script>
        tailwind.config = {{
            darkMode: 'class',
        }}
    </script>
</head>
<body class="min-h-screen flex flex-col">
    <!-- 헤더 섹션: 배경 이미지를 body로 옮기고 hero-security 클래스 제거 -->
    <header class="text-white py-20 px-6 relative overflow-hidden">
        
        <!-- 좌측 상단 브랜드 로고: Putto's Lectures -->
        <div class="absolute top-6 left-6 md:left-10 flex items-center space-x-3 z-20">
            <i class="fas fa-terminal text-cyan-400 text-xl"></i>
            <span class="font-bold text-slate-100 tracking-widest font-mono text-sm md:text-base">PUTTO'S LECTURES</span>
        </div>

        <div class="max-w-4xl mx-auto relative z-10 text-center mt-4">
            <div class="inline-flex items-center justify-center space-x-3 mb-6 bg-slate-900/50 p-3 rounded-2xl backdrop-blur-sm border border-slate-700">
                <!-- 아이콘 변경: 방패(보안) 및 터미널(해킹) 아이콘 사용 -->
                <i class="fas fa-user-secret text-4xl text-cyan-400"></i>
                <span class="text-slate-400">|</span>
                <i class="fas fa-shield-halved text-4xl text-blue-500"></i>
            </div>
            
            <!-- 타이틀 텍스트: bg-clip-text 사용 시 꼬리가 잘리지 않도록 pb-2 추가 -->
            <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2 pb-2 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-600">
                Cloud Security & Hacking Lab
            </h1>
            
            <!-- 한글 서브 타이틀: 위 타이틀과 간격을 띄우기 위해 mt-6 추가 및 텍스트 밝기 상향 -->
            <p class="mt-6 text-slate-200 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
                실전 클라우드 인프라 보안 및 모의 해킹 시나리오 연구 자료 저장소
            </p>
        </div>
        <!-- 배경 장식용 희미한 그리드 패턴 -->
        <div class="absolute inset-0 bg-[url('https://tailwindcss.com/_next/static/media/hero-dark.9a75e138.png')] opacity-20 z-0 pointer-events-none"></div>
    </header>

    <!-- 메인 콘텐츠 영역: 리스트 크기 축소 및 컴팩트한 디자인 적용 -->
    <main class="flex-grow max-w-4xl mx-auto px-6 py-12 w-full">
"""

    html_footer = """
    </main>
    <!-- 푸터: 다크 테마 적용 -->
    <footer class="border-t border-slate-800/50 py-8 text-center text-slate-500 text-sm bg-slate-950/80 backdrop-blur-sm">
        <p class="font-mono">&copy; 2026 Putto's Lectures. All rights reserved. <span class="text-cyan-900">| Access Secured.</span></p>
    </footer>
</body>
</html>
"""

    content_body = ""
    structure = {}
    
    # ---------------------------------------------------------------------------
    # 1. 마크다운(.md) 파일을 찾아 HTML 파일로 사전 변환
    # ---------------------------------------------------------------------------
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                md_path = os.path.join(root, file)
                html_filename = file.replace('.md', '.html')
                html_path = os.path.join(root, html_filename)

                with open(md_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()

                # 마크다운 변환
                md_html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

                # 개별 문서 디자인 변경: 다크 모드 문서 스타일(prose-invert) 적용 및 컨테이너 배경색 어둡게 변경
                doc_content = f'''
                <div class="bg-slate-900/80 p-8 rounded-2xl shadow-xl border border-slate-800 backdrop-blur-sm prose prose-invert prose-slate max-w-none prose-img:rounded-xl prose-a:text-cyan-400 hover:prose-a:text-cyan-300 prose-headings:text-slate-100">
                    {md_html}
                </div>
                '''
                full_doc_html = html_header + doc_content + html_footer

                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(full_doc_html)

    # ---------------------------------------------------------------------------
    # 2. 저장소 탐색 및 데이터 구조화
    # ---------------------------------------------------------------------------
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_path = os.path.relpath(root, '.')
        html_files = sorted([f for f in files if f.endswith('.html') and f not in exclude_files])
        if html_files:
            structure[rel_path] = html_files

    # ---------------------------------------------------------------------------
    # 3. 루트 인덱스 HTML 생성
    # ---------------------------------------------------------------------------
    for folder in sorted(structure.keys()):
        files = structure[folder]
        display_folder = "Root Directory" if folder == "." else folder
        folder_icon = "fa-folder-tree" if folder != "." else "fa-server"
        
        # 섹션 헤더 크기 축소 및 스타일 변경
        content_body += f"""
        <section class="mb-8">
            <div class="flex items-center space-x-3 mb-4 border-b border-slate-800/80 pb-2">
                <i class="fas {folder_icon} text-cyan-600 text-lg"></i>
                <h2 class="text-lg font-bold text-slate-300">{display_folder}</h2>
                <span class="text-slate-500 text-xs font-mono ml-2">[{len(files)} objects]</span>
            </div>
            <!-- 박스 형태 제거: 단순하고 세련된 텍스트 리스트 형태로 변경 -->
            <ul class="space-y-1 font-mono text-sm">
        """
        
        # 파일 목록 디자인 변경: 박스 제거 및 터미널 라인 스타일 적용
        for file in files:
            file_path = os.path.join(folder, file) if folder != "." else file
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            content_body += f"""
                <li>
                    <a href="{file_path}" target="_blank" class="list-hover flex items-center py-2 px-3 rounded border-l-2 border-transparent hover:border-cyan-500 group">
                        <span class="text-slate-600 mr-3 group-hover:text-cyan-400 transition-colors">
                            <i class="fas fa-chevron-right text-xs"></i>
                        </span>
                        <span class="text-slate-300 group-hover:text-cyan-300 transition-colors">{display_name}</span>
                        <span class="ml-auto text-slate-600 text-xs opacity-0 group-hover:opacity-100 transition-opacity">/{file}</span>
                    </a>
                </li>
            """
            
        content_body += """
            </ul>
        </section>
        """

    # 최종 파일 작성
    full_html = html_header + content_body + html_footer
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"System Log: {datetime.now().strftime('%H:%M:%S')} - Index generation complete. Security protocols active.")

if __name__ == "__main__":
    generate_index()
