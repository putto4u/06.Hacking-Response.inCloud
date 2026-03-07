import os
import markdown
from datetime import datetime

def generate_index():
    # 제외할 폴더 및 파일 설정 (기능 유지)
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
        }}

        /* 해킹/보안 분위기의 히어로 섹션 배경 이미지 및 오버레이 설정 */
        .hero-security {{
            /* 배경 이미지 URL: 사이버 보안 컨셉의 무료 이미지 사용 (필요시 변경 가능) */
            background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 1)), 
                              url('https://images.unsplash.com/photo-1563986768609-322da13575f3?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
        }}

        /* 카드 호버 효과: 약간 떠오르며 밝은 테두리 강조 */
        .card-hover {{
            transition: all 0.3s ease;
            border: 1px solid #1e293b; /* 기본 어두운 테두리 */
        }}
        .card-hover:hover {{
            transform: translateY(-4px);
            border-color: #0ea5e9; /* 호버 시 사이안(Cyan) 색상 테두리 강조 */
            box-shadow: 0 10px 30px -10px rgba(14, 165, 233, 0.3); /* 사이안 색상 그림자 */
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
    <!-- 헤더 섹션: 보안 테마 적용 및 강조 -->
    <header class="hero-security text-white py-20 px-6 relative overflow-hidden">
        <div class="max-w-4xl mx-auto relative z-10 text-center">
            <div class="inline-flex items-center justify-center space-x-3 mb-6 bg-slate-900/50 p-3 rounded-2xl backdrop-blur-sm border border-slate-700">
                <!-- 아이콘 변경: 방패(보안) 및 터미널(해킹) 아이콘 사용 -->
                <i class="fas fa-user-secret text-4xl text-cyan-400"></i>
                <span class="text-slate-400">|</span>
                <i class="fas fa-shield-halved text-4xl text-blue-500"></i>
            </div>
            <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-600">
                Cloud Security & Hacking Lab
            </h1>
            <p class="text-slate-300 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
                실전 클라우드 인프라 보안 및 모의 해킹 시나리오 연구 자료 저장소
            </p>
            <div class="mt-8 flex items-center justify-center text-sm text-slate-400 font-mono bg-black/30 inline-block px-4 py-2 rounded-full">
                <i class="far fa-clock mr-2 text-cyan-500"></i>
                <span>System Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
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
    <footer class="border-t border-slate-800/50 py-8 text-center text-slate-500 text-sm bg-slate-950">
        <p class="font-mono">&copy; 2026 Security & Cloud Hacking Lab. All rights reserved. <span class="text-cyan-900">| Access Secured.</span></p>
    </footer>
</body>
</html>
"""

    content_body = ""
    structure = {}
    
    # ---------------------------------------------------------------------------
    # 1. 마크다운(.md) 파일을 찾아 HTML 파일로 사전 변환 (기능 유지, 디자인만 변경)
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
    # 2. 저장소 탐색 및 데이터 구조화 (기능 유지)
    # ---------------------------------------------------------------------------
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_path = os.path.relpath(root, '.')
        html_files = sorted([f for f in files if f.endswith('.html') and f not in exclude_files])
        if html_files:
            structure[rel_path] = html_files

    # ---------------------------------------------------------------------------
    # 3. 루트 인덱스 HTML 생성 (디자인 변경: 리스트 강조 축소 및 컴팩트화)
    # ---------------------------------------------------------------------------
    for folder in sorted(structure.keys()):
        files = structure[folder]
        display_folder = "Root Directory" if folder == "." else folder
        folder_icon = "fa-folder-tree" if folder != "." else "fa-server"
        
        # 섹션 헤더 크기 축소 및 스타일 변경
        content_body += f"""
        <section class="mb-8">
            <div class="flex items-center space-x-3 mb-4 border-b border-slate-800 pb-2">
                <i class="fas {folder_icon} text-cyan-600 text-lg"></i>
                <h2 class="text-lg font-bold text-slate-300">{display_folder}</h2>
                <span class="bg-slate-800 text-slate-400 text-xs font-mono px-2 py-1 rounded-md border border-slate-700">{len(files)} Files</span>
            </div>
            <!-- 그리드 레이아웃: 카드를 더 작고 조밀하게 배치 (gap 줄임) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        """
        
        # 파일 카드 디자인 변경: 어둡고 컴팩트하게
        for file in files:
            file_path = os.path.join(folder, file) if folder != "." else file
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            content_body += f"""
                <a href="{file_path}" target="_blank" class="card-hover bg-slate-900/50 p-4 rounded-lg shadow-sm flex items-center space-x-4 group">
                    <div class="bg-slate-800/80 p-2 rounded-md text-cyan-500 group-hover:text-cyan-300 transition-colors">
                        <i class="fas fa-file-shield text-lg"></i>
                    </div>
                    <div class="overflow-hidden flex-grow">
                        <h3 class="font-medium text-slate-200 truncate text-sm group-hover:text-white transition-colors" title="{display_name}">{display_name}</h3>
                        <p class="text-[10px] text-slate-500 mt-0.5 truncate font-mono">/{file}</p>
                    </div>
                    <div class="text-slate-600 group-hover:text-cyan-400 transition-colors text-sm">
                        <i class="fas fa-chevron-right"></i>
                    </div>
                </a>
            """
            
        content_body += """
            </div>
        </section>
        """

    # 최종 파일 작성
    full_html = html_header + content_body + html_footer
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"System Log: {datetime.now().strftime('%H:%M:%S')} - Index generation complete. Security protocols active.")

if __name__ == "__main__":
    generate_index()
