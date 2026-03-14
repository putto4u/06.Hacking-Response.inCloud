import os
import markdown
from datetime import datetime

def generate_index():
    # 제외할 폴더 및 파일 설정
    exclude_dirs = {'.git', '.github', '.pytest_cache', '__pycache__', 'assets'}
    exclude_files = {'index.html', 'generate_index.py', 'genindex.py', 'README.md'}
    
    # 디자인 테마 변경: 가시성을 높인 어두운 테마 및 저자(Putto) 강조 디자인 적용
    html_header = f"""<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security & Cloud Hacking Lab</title>
    <!-- Tailwind CSS (테일윈드 씨에스에스) 및 Typography (타이포그래피) 플러그인 로드 -->
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <!-- Font Awesome (폰트 어썸) 아이콘 로드 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Web Fonts (구글 웹 폰트) 로드 -->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        
        /* 기본 글꼴 및 다크 모드 배경색 설정 */
        body {{ 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: #020617; 
            color: #f8fafc; 
            /* 전체 화면 배경 이미지 적용 및 투명도(Overlay) 설정: 텍스트 가시성을 위해 어두운 오버레이 강화 */
            background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.75), rgba(2, 6, 23, 0.95)), 
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
            color: #22d3ee; 
            padding-left: 0.75rem; 
            background-color: rgba(15, 23, 42, 0.8); 
            border-left-color: #0ea5e9;
        }}

        /* 텍스트 가시성을 높이는 그림자 효과 클래스 */
        .text-glow {{
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
        }}
        .neon-glow {{
            text-shadow: 0 0 8px rgba(34, 211, 238, 0.6);
        }}
    </style>
    <!-- Tailwind (테일윈드) 설정 커스터마이징 -->
    <script>
        tailwind.config = {{
            darkMode: 'class',
        }}
    </script>
</head>
<body class="min-h-screen flex flex-col">
    <!-- 헤더 섹션 -->
    <header class="py-24 px-6 relative overflow-hidden">
        
        <!-- 좌측 상단 브랜드 로고: 강사/저자 Putto 디자인 강화 (터미널 뱃지 스타일) -->
        <div class="absolute top-6 left-6 md:left-10 z-20 group cursor-default">
            <div class="flex items-center space-x-2 bg-slate-900/80 py-2 px-4 rounded-xl border border-cyan-900/50 backdrop-blur-md shadow-[0_0_15px_rgba(8,145,178,0.2)] transition-all duration-300 group-hover:border-cyan-400/60 group-hover:shadow-[0_0_20px_rgba(34,211,238,0.4)]">
                <!-- 활성화 상태를 나타내는 깜빡이는 신호(Ping) 효과 -->
                <div class="relative flex h-3 w-3 mr-1">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
                </div>
                <span class="font-mono text-[10px] md:text-xs text-slate-400 tracking-wider">CHIEF ARCHITECT <span class="text-cyan-500 ml-1">❯</span></span>
                <span class="font-black text-cyan-300 tracking-widest font-mono text-sm md:text-base neon-glow ml-1">PUTTO</span>
                <span class="font-bold text-slate-200 tracking-widest font-mono text-sm md:text-base">'S LECTURES</span>
            </div>
        </div>

        <div class="max-w-4xl mx-auto relative z-10 text-center mt-8">
            <div class="inline-flex items-center justify-center space-x-3 mb-8 bg-slate-950/60 p-4 rounded-2xl backdrop-blur-md border border-slate-700/80 shadow-2xl">
                <!-- 방패(보안) 및 터미널(해킹) 아이콘 -->
                <i class="fas fa-user-secret text-4xl text-cyan-400 drop-shadow-lg"></i>
                <span class="text-slate-500">|</span>
                <i class="fas fa-shield-halved text-4xl text-blue-500 drop-shadow-lg"></i>
            </div>
            
            <!-- 타이틀 텍스트: 그라데이션 및 강한 텍스트 그림자(Drop Shadow) 적용으로 배경과 분리 -->
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-black tracking-tight mb-2 pb-2 bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-400 drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
                Cloud Security & Hacking Lab
            </h1>
            
            <!-- 한글 서브 타이틀: 폰트 두께 상향 및 밝기 조정 -->
            <p class="mt-8 text-slate-100 font-medium text-lg md:text-xl max-w-2xl mx-auto leading-relaxed text-glow">
                실전 클라우드 인프라 보안 및 모의 해킹 시나리오 연구 자료 저장소
            </p>
        </div>
    </header>

    <!-- 메인 콘텐츠 영역 -->
    <main class="flex-grow max-w-4xl mx-auto px-6 py-8 w-full">
"""

    html_footer = """
    </main>
    <!-- 푸터 -->
    <footer class="border-t border-slate-800/80 py-8 text-center text-slate-400 text-sm bg-slate-950/90 backdrop-blur-md mt-auto">
        <p class="font-mono">&copy; 2026 Putto's Lectures. All rights reserved. <span class="text-cyan-800 font-bold ml-2">| ACCESS SECURED.</span></p>
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

                # 개별 문서 디자인: 가독성을 위해 문서 컨테이너 배경을 더 짙게 처리
                doc_content = f'''
                <div class="bg-slate-950/90 p-8 md:p-12 rounded-2xl shadow-2xl border border-slate-700/50 backdrop-blur-xl prose prose-invert prose-slate max-w-none prose-img:rounded-xl prose-a:text-cyan-400 hover:prose-a:text-cyan-300 prose-headings:text-slate-100 prose-strong:text-cyan-100">
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
        
        content_body += f"""
        <section class="mb-10 bg-slate-900/60 p-6 rounded-2xl border border-slate-800/80 backdrop-blur-sm shadow-xl">
            <div class="flex items-center space-x-3 mb-4 border-b border-slate-700/80 pb-3">
                <i class="fas {folder_icon} text-cyan-500 text-xl drop-shadow-md"></i>
                <h2 class="text-xl font-bold text-slate-100 tracking-wide text-glow">{display_folder}</h2>
                <span class="text-cyan-600/80 text-xs font-mono ml-2 font-bold">[{len(files)} OBJECTS]</span>
            </div>
            
            <ul class="space-y-2 font-mono text-sm md:text-base">
        """
        
        for file in files:
            file_path = os.path.join(folder, file) if folder != "." else file
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            content_body += f"""
                <li>
                    <a href="{file_path}" target="_blank" class="list-hover flex items-center py-3 px-4 rounded-lg border-l-4 border-transparent bg-slate-950/40 group">
                        <span class="text-slate-500 mr-4 group-hover:text-cyan-400 transition-colors">
                            <i class="fas fa-chevron-right text-xs"></i>
                        </span>
                        <span class="text-slate-200 font-medium group-hover:text-cyan-300 transition-colors drop-shadow-sm">{display_name}</span>
                        <span class="ml-auto text-slate-600 text-xs opacity-0 group-hover:opacity-100 transition-opacity tracking-widest">/{file}</span>
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
