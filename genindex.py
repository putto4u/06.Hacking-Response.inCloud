<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>메타스플로잇터블2 및 버추얼박스 구축 가이드</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: #f8fafc;import os
import markdown
from datetime import datetime

def generate_index():
    exclude_dirs = {'.git', '.github', '.pytest_cache', '__pycache__', 'assets'}
    exclude_files = {'index.html', 'generate_index.py', 'genindex.py', 'README.md', 'toc.html'}
    
    # ---------------------------------------------------------------------------
    # [1] 마크다운 변환 문서용 기본 HTML(HyperText Markup Language, 웹페이지 구조 언어) 헤더/푸터
    # ---------------------------------------------------------------------------
    doc_html_header = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: transparent; 
            color: #f8fafc; 
            margin: 0; padding: 0;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #0ea5e9; }
    </style>
    <script>tailwind.config = { darkMode: 'class' }</script>
</head>
<body class="p-6 pt-20 md:p-10 md:pt-24 max-w-5xl mx-auto">
"""
    doc_html_footer = "</body></html>"

    # ---------------------------------------------------------------------------
    # [2] 동적 생성 TOC(Table of Contents, 목차) 전용 HTML 헤더
    # ---------------------------------------------------------------------------
    toc_html_header = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: transparent; 
            color: #f8fafc; 
            margin: 0; padding: 0;
        }
        .list-hover { transition: all 0.2s ease; }
        .list-hover:hover {
            color: #22d3ee; padding-left: 0.75rem; 
            background-color: rgba(15, 23, 42, 0.8); border-left-color: #0ea5e9;
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #0ea5e9; }
        .text-glow { text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8); }
    </style>
    <script>tailwind.config = { darkMode: 'class' }</script>
</head>
<body class="p-6 pt-20 md:p-12 md:pt-24">

    <!-- 첫 화면(TOC) 전용 메인 타이틀 섹션 -->
    <div class="max-w-6xl mx-auto text-center mb-10 md:mb-14">
        <h1 class="text-3xl md:text-4xl lg:text-5xl font-black tracking-tight mb-2 pb-1 bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-400 drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
            Cloud Security & Hacking Lab
        </h1>
        <p class="text-slate-300 font-medium text-sm md:text-base max-w-2xl mx-auto text-glow">
            실전 클라우드 인프라 보안 및 모의 해킹 시나리오 연구 자료 저장소
        </p>
    </div>

    <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-8 border-b border-slate-700/80 pb-4">
            <h1 class="text-2xl md:text-3xl font-black text-slate-100 tracking-wide">
                <i class="fas fa-network-wired text-cyan-500 mr-3"></i>DIRECTORY INDEX
            </h1>
            <!-- 초기 상태가 닫혀있으므로 '펼치기(EXPAND ALL)' 액션을 유도하는 텍스트 및 열린 폴더 아이콘 적용 -->
            <button onclick="toggleAllFolders()" class="group flex items-center space-x-2 bg-slate-800/80 hover:bg-slate-700 text-cyan-400 py-2 px-4 rounded-lg border border-cyan-900/50 transition-all duration-300 shadow-md">
                <i class="fas fa-folder-open" id="global-toggle-icon"></i>
                <span class="font-mono text-xs font-bold tracking-widest" id="global-toggle-text">EXPAND ALL</span>
            </button>
        </div>
        <div class="space-y-6">
"""

    # ---------------------------------------------------------------------------
    # JS(JavaScript, 자바스크립트) 제어 로직
    # 인라인 스타일(style="grid-template-rows") 기반 상태 판단 및 제어 적용
    # ---------------------------------------------------------------------------
    toc_html_footer = """
        </div>
    </div>
    
    <script>
        // 초기 렌더링 상태가 축소(Collapse)이므로 상태 변수를 false로 초기화
        let isAllExpanded = false;
        
        function toggleFolder(element) {
            const section = element.closest('.folder-section');
            const listContainer = section.querySelector('.list-container');
            const folderIcon = element.querySelector('.folder-icon');
            const chevronIcon = element.querySelector('.chevron-icon');
            const baseIcon = element.getAttribute('data-base-icon');
            
            // CSS Grid 인라인 속성값을 직접 확인하여 Tailwind JIT 컴파일 오류 원천 회피
            const isExpanded = listContainer.style.gridTemplateRows === '1fr';

            if (isExpanded) {
                // 축소(Collapse) 상태로 전환
                listContainer.style.gridTemplateRows = '0fr';
                listContainer.classList.remove('opacity-100', 'border-slate-700/80');
                listContainer.classList.add('opacity-0', 'border-transparent');
                
                chevronIcon.classList.remove('fa-chevron-up');
                chevronIcon.classList.add('fa-chevron-down');
                
                if (baseIcon !== 'fa-server') {
                    folderIcon.classList.remove('fa-folder-open');
                    folderIcon.classList.add('fa-folder');
                }
            } else {
                // 확장(Expand) 상태로 전환
                listContainer.style.gridTemplateRows = '1fr';
                listContainer.classList.remove('opacity-0', 'border-transparent');
                listContainer.classList.add('opacity-100', 'border-slate-700/80');
                
                chevronIcon.classList.remove('fa-chevron-down');
                chevronIcon.classList.add('fa-chevron-up');
                
                if (baseIcon !== 'fa-server') {
                    folderIcon.classList.remove('fa-folder');
                    folderIcon.classList.add('fa-folder-open');
                }
            }
        }

        function toggleAllFolders() {
            isAllExpanded = !isAllExpanded;
            const headers = document.querySelectorAll('.folder-header');
            const globalBtnIcon = document.getElementById('global-toggle-icon');
            const globalBtnText = document.getElementById('global-toggle-text');

            headers.forEach(header => {
                const section = header.closest('.folder-section');
                const listContainer = section.querySelector('.list-container');
                const isCurrentlyExpanded = listContainer.style.gridTemplateRows === '1fr';
                
                if (isAllExpanded !== isCurrentlyExpanded) {
                    toggleFolder(header);
                }
            });

            if (isAllExpanded) {
                // 전체가 확장된 상태이므로, 버튼은 '모두 축소(COLLAPSE ALL)' 액션을 유도하도록 변경
                globalBtnIcon.classList.remove('fa-folder-open');
                globalBtnIcon.classList.add('fa-folder');
                globalBtnText.innerText = 'COLLAPSE ALL';
            } else {
                // 전체가 축소된 상태이므로, 버튼은 '모두 확장(EXPAND ALL)' 액션을 유도하도록 변경
                globalBtnIcon.classList.remove('fa-folder');
                globalBtnIcon.classList.add('fa-folder-open');
                globalBtnText.innerText = 'EXPAND ALL';
            }
        }
    </script>
</body>
</html>
"""

    # ---------------------------------------------------------------------------
    # [3] 단일 화면 레이아웃 (Iframe을 전체 영역으로 확장) 메인 HTML 헤더/푸터
    # ---------------------------------------------------------------------------
    index_html = f"""<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security & Cloud Hacking Lab</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        body {{ 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: #020617; 
            background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.98)), 
                              url('image_1a3201.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center center;
            margin: 0; padding: 0;
            height: 100vh;
            width: 100vw;
            overflow: hidden; 
        }}
        .neon-glow {{ text-shadow: 0 0 8px rgba(34, 211, 238, 0.6); }}
    </style>
    <script>tailwind.config = {{ darkMode: 'class' }}</script>
</head>
<body class="relative">
    <!-- 떠있는 저자 박스 (어디서든 목차로 복귀 가능) -->
    <a href="toc.html" target="content-frame" class="absolute top-5 right-5 md:top-6 md:right-8 z-50 group cursor-pointer block">
        <div class="flex items-center space-x-1.5 bg-slate-900/80 py-1.5 px-3 rounded-lg border border-cyan-900/50 backdrop-blur-md shadow-[0_0_10px_rgba(8,145,178,0.2)] transition-all duration-300 group-hover:border-cyan-400/60 group-hover:shadow-[0_0_15px_rgba(34,211,238,0.4)]">
            <div class="relative flex h-2 w-2 mr-0.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </div>
            <span class="font-mono text-[8px] md:text-[10px] text-slate-400 tracking-wider">CHIEF SYSTEM ARCHITECT <span class="text-cyan-500 ml-0.5">❯</span></span>
            <span class="font-black text-cyan-300 tracking-widest font-mono text-xs md:text-sm neon-glow ml-0.5">PUTTO</span>
            <span class="font-bold text-slate-200 tracking-widest font-mono text-xs md:text-sm">'S LECTURES</span>
        </div>
    </a>

    <!-- 전체 화면 Iframe (목차 및 개별 문서 출력 영역) -->
    <iframe name="content-frame" id="content-frame" class="absolute inset-0 w-full h-full border-none z-10 bg-transparent" src="toc.html"></iframe>
</body>
</html>
"""

    structure = {}
    toc_body = ""
    
    # ---------------------------------------------------------------------------
    # [4] 마크다운 변환 및 개별 HTML 파일 생성
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

                md_html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

                doc_content = f'''
                <div class="prose prose-invert prose-slate max-w-none prose-img:rounded-xl prose-a:text-cyan-400 hover:prose-a:text-cyan-300 prose-headings:text-slate-100 prose-strong:text-cyan-100 bg-slate-900/40 p-8 rounded-2xl border border-slate-700/50 shadow-xl">
                    {md_html}
                </div>
                '''
                
                full_doc_html = doc_html_header + doc_content + doc_html_footer

                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(full_doc_html)

    # ---------------------------------------------------------------------------
    # [5] 디렉토리 탐색 및 HTML 기반 목차(TOC) 생성 (사이드바 스타일 적용)
    # ---------------------------------------------------------------------------
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_path = os.path.relpath(root, '.')
        html_files = sorted([f for f in files if f.endswith('.html') and f not in exclude_files])
        if html_files:
            structure[rel_path] = html_files

    for folder in sorted(structure.keys()):
        files = structure[folder]
        is_root = folder == "."
        display_folder = "Root Directory" if is_root else folder
        
        base_icon = "fa-server" if is_root else "fa-folder-open"
        closed_icon = "fa-server" if is_root else "fa-folder"
        
        # 렌더링 시점에 보여질 초기 아이콘 (루트 서버를 제외하고 닫힌 폴더로 렌더링)
        initial_folder_icon = "fa-server" if is_root else "fa-folder"
        
        # 목차 내 개별 폴더 섹션 구성 
        # grid-template-rows: 0fr 인라인 스타일을 강제 삽입하여 초기 렌더링 시 완벽한 숨김 처리 보장
        # 화살표 아이콘을 명시적인 fa-chevron-down 으로 설정
        toc_body += f"""
        <div class="folder-section bg-slate-900/60 rounded-xl border border-slate-700/80 shadow-lg transition-all duration-300">
            <div class="folder-header flex items-center p-4 cursor-pointer group hover:bg-slate-800/80 rounded-t-xl transition-colors" 
                 onclick="toggleFolder(this)" 
                 data-base-icon="{base_icon}">
                <i class="folder-icon fas {initial_folder_icon} text-cyan-500 w-6 text-center text-lg transition-transform duration-300 group-hover:scale-110"></i>
                <h2 class="text-base font-bold text-slate-200 ml-3 group-hover:text-cyan-300 tracking-wide">{display_folder}</h2>
                <span class="text-cyan-600/80 text-[10px] font-mono ml-3 font-bold bg-slate-950/50 px-2 py-1 rounded-md">[{len(files)}]</span>
                <i class="fas fa-chevron-down ml-auto text-slate-500 text-sm transition-transform duration-300 chevron-icon"></i>
            </div>
            
            <div class="list-container grid transition-all duration-300 ease-in-out opacity-0 border-t border-transparent" style="grid-template-rows: 0fr;">
                <div class="overflow-hidden bg-slate-950/40 rounded-b-xl">
                    <ul class="py-2">
        """
        
        for file in files:
            file_path = os.path.join(folder, file) if not is_root else file
            display_name = file.replace('.html', '').replace('_', ' ').replace('-', ' ')
            
            toc_body += f"""
                        <li>
                            <a href="{file_path}" class="list-hover flex items-center py-3 px-5 border-l-2 border-transparent group text-sm">
                                <i class="fas fa-file-code text-slate-600 mr-3 group-hover:text-cyan-400"></i>
                                <span class="text-slate-300 font-medium group-hover:text-cyan-100">{display_name}</span>
                            </a>
                        </li>
            """
            
        toc_body += """
                    </ul>
                </div>
            </div>
        </div>
        """

    # ---------------------------------------------------------------------------
    # [6] 메인 index.html 및 목차용 toc.html 파일 작성
    # ---------------------------------------------------------------------------
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    full_toc_html = toc_html_header + toc_body + toc_html_footer
    with open('toc.html', 'w', encoding='utf-8') as f:
        f.write(full_toc_html)
    
    print(f"System Log: {datetime.now().strftime('%H:%M:%S')} - Layout updated. Inline styles enforced for robust collapsing.")

if __name__ == "__main__":
    generate_index()
            color: #1e293b;
            line-height: 1.8;
        }
        .textbook-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .page-block {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            padding: 50px;
            margin-bottom: 60px;
        }
        .chapter-title {
            color: #0f172a;
            font-size: 2.25rem;
            font-weight: 800;
            border-bottom: 4px solid #3b82f6;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .section-title {
            color: #1d4ed8;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        .step-title {
            font-weight: 700;
            color: #334155;
            font-size: 1.25rem;
            margin-top: 25px;
        }
        .content-block {
            margin-bottom: 25px;
            font-size: 1.05rem;
        }
        .image-placeholder {
            background-color: #e2e8f0;
            border: 2px dashed #94a3b8;
            border-radius: 8px;
            height: 300px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 30px 0 10px 0;
            color: #475569;
            font-weight: 500;
            font-size: 1.1rem;
            text-align: center;
            padding: 20px;
        }
        .source-link {
            text-align: center;
            font-size: 0.95rem;
            color: #64748b;
            margin-bottom: 35px;
        }
        .source-link a {
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }
        .source-link a:hover {
            text-decoration: underline;
            color: #2563eb;
        }
        .explanation-box {
            background-color: #f0fdf4;
            border-left: 5px solid #22c55e;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
        }
        .warning-box {
            background-color: #fef2f2;
            border-left: 5px solid #ef4444;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
        }
        .tip-box {
            background-color: #eff6ff;
            border-left: 5px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-size: 0.95rem;
        }
        .menu-path {
            background-color: #f1f5f9;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: monospace;
            font-weight: 600;
            color: #0ea5e9;
        }
        .highlight {
            font-weight: 700;
            color: #b91c1c;
        }
        a {
            color: #2563eb;
            text-decoration: underline;
        }
        a:hover {
            color: #1d4ed8;
        }
    </style>
</head>
<body>

<div class="textbook-container">

    <!-- Page 1: Introduction and Download -->
    <div class="page-block" id="page-1">
        <h1 class="chapter-title">메타스플로잇터블2 및 버추얼박스 환경 구축</h1>
        
        <div class="content-block">
            이 과정에서는 정보 보안 및 모의해킹 실습을 위한 필수 인프라인 메타스플로잇터블2를 버추얼박스 가상 환경에 구축하는 방법을 단계별로 상세히 다룹니다.
            안전한 샌드박스 환경을 구성하여 실제 운영 환경에 영향을 주지 않고 취약점 분석을 수행할 수 있는 기반을 마련합니다.
        </div>

        <div class="warning-box">
            <strong>[필독] 보안 아키텍트의 경고</strong><br>
            메타스플로잇터블2는 의도적으로 심각한 취약점들을 포함하도록 설계된 OS (Operating System, 운영체제)입니다. 
            절대로 인터넷에 직접 연결된 공인 IP (Internet Protocol, 인터넷 규약) 네트워크나, 신뢰할 수 없는 사용자가 접근 가능한 사내 네트워크에 브릿지 모드로 연결해서는 안 됩니다. 
            반드시 Host-Only (Host-Only Network, 호스트 전용 네트워크) 환경에서만 격리하여 운영해야 합니다.
        </div>

        <h2 class="section-title">1. 메타스플로잇터블2 다운로드</h2>
        
        <div class="content-block">
            메타스플로잇터블2는 보안 솔루션 기업인 Rapid7 (래피드세븐)에서 제공하며, 공식 소스포지(SourceForge) 저장소를 통해 안전하게 다운로드할 수 있습니다.
        </div>

        <div class="image-placeholder">
            <span>[스냅샷 삽입: 메타스플로잇터블2 소스포지 다운로드 화면]</span>
            <span class="text-sm text-slate-400 mt-2 font-normal">이곳에 다운로드 페이지 캡처 이미지를 삽입하세요.</span>
        </div>
        <div class="source-link">
            캡처 참조 출처: <a href="https://sourceforge.net/projects/metasploitable/" target="_blank" rel="noopener noreferrer">SourceForge - Metasploitable 다운로드 페이지</a>
        </div>

        <div class="content-block">
            <span class="step-title">Step 1-1. 다운로드 페이지 접속</span><br>
            공식 배포처인 <a href="https://sourceforge.net/projects/metasploitable/" target="_blank" rel="noopener noreferrer">SourceForge 메타스플로잇터블 페이지</a>로 이동합니다.
            화면 중앙의 초록색 <span class="highlight">Download Latest Version</span> 버튼을 클릭합니다.
        </div>

        <div class="content-block">
            <span class="step-title">Step 1-2. 파일 압축 해제</span><br>
            다운로드된 파일은 <code>metasploitable-linux-2.0.0.zip</code> 형태의 압축 파일입니다.
            원하는 실습용 폴더(예: <code>C:\VMs\Metasploitable2</code>)를 생성하고 압축을 해제합니다.
        </div>

        <div class="explanation-box">
            <strong>용어 해설: VMDK 란?</strong><br>
            압축을 해제하면 <code>.vmdk</code> (Virtual Machine Disk, 가상 머신 디스크) 확장자를 가진 파일이 나타납니다. 
            이는 가상 머신의 하드 드라이브 역할을 하는 파일로, 운영체제와 데이터가 모두 포함된 이미지입니다. 
            우리는 ISO 파일을 이용해 OS를 처음부터 설치하는 것이 아니라, 이미 설치가 완료된 이 디스크 이미지를 버추얼박스에 '연결'만 하여 즉시 사용할 것입니다.
        </div>
    </div>

    <!-- Page 2: VirtualBox VM Creation -->
    <div class="page-block" id="page-2">
        <h2 class="section-title">2. 버추얼박스 가상 머신 생성 및 설정</h2>

        <div class="content-block">
            다운로드한 가상 디스크 파일을 실행하기 위해 오라클 버추얼박스(Oracle VirtualBox)에 새로운 가상 환경을 구성합니다. 
            버추얼박스가 설치되어 있지 않다면 <a href="https://www.virtualbox.org/" target="_blank" rel="noopener noreferrer">버추얼박스 공식 홈페이지</a>에서 다운로드하여 설치합니다.
        </div>

        <div class="image-placeholder">
            <span>[스냅샷 삽입: 버추얼박스 가상 머신 만들기 - 이름 및 운영체제 설정 화면]</span>
            <span class="text-sm text-slate-400 mt-2 font-normal">이곳에 버추얼박스 '새로 만들기' 마법사 캡처 이미지를 삽입하세요.</span>
        </div>
        <div class="source-link">
            캡처 참조 출처: <a href="https://www.virtualbox.org/manual/ch01.html#gui-createvm" target="_blank" rel="noopener noreferrer">VirtualBox 공식 매뉴얼 - 가상 머신 생성 가이드</a>
        </div>

        <div class="content-block">
            <span class="step-title">Step 2-1. 가상 머신 만들기 실행</span><br>
            버추얼박스 관리자를 실행하고 상단 메뉴에서 <span class="menu-path">머신(M) > 새로 만들기(N)</span>를 클릭하거나, 아이콘 메뉴 중 <strong>[새로 만들기]</strong> 아이콘을 클릭합니다.
        </div>

        <div class="content-block">
            <span class="step-title">Step 2-2. 이름 및 운영체제 종류 설정</span><br>
            새 가상 머신 생성 마법사가 나타나면 아래와 같이 정확히 입력합니다.
            <ul class="list-disc ml-8 mt-2 space-y-2">
                <li><strong>이름:</strong> <code>Metasploitable2</code> (원하는 이름으로 지정 가능하나 식별을 위해 권장)</li>
                <li><strong>머신 폴더:</strong> 기본값 유지 (또는 용량이 넉넉한 드라이브 지정)</li>
                <li><strong>종류:</strong> <code>Linux</code> 선택</li>
                <li><strong>버전:</strong> <code>Ubuntu (32-bit)</code> 선택 <span class="highlight">(매우 중요)</span></li>
            </ul>
        </div>

        <div class="tip-box">
            <strong>실전 팁: 왜 64-bit가 아닌 32-bit를 선택하나요?</strong><br>
            메타스플로잇터블2는 우분투 8.04 LTS (Long Term Support, 장기 지원) 버전의 32비트 아키텍처를 기반으로 제작되었습니다. 
            만약 64-bit로 설정할 경우, 커널 패닉(Kernel Panic, 운영체제 핵심부 치명적 오류)이 발생하여 부팅이 불가능할 수 있습니다. 
            항상 타겟 시스템의 아키텍처를 정확히 파악하고 환경을 구성하는 것이 아키텍트의 기본입니다.
        </div>

        <div class="content-block">
            <span class="step-title">Step 2-3. 메모리(RAM) 크기 할당</span><br>
            메타스플로잇터블2는 GUI (Graphical User Interface, 그래픽 사용자 인터페이스)가 없는 CLI (Command Line Interface, 명령줄 인터페이스) 환경이므로 많은 자원을 요구하지 않습니다.
            <ul class="list-disc ml-8 mt-2">
                <li><strong>메모리 크기:</strong> <code>512 MB</code> 또는 <code>1024 MB</code>로 슬라이더를 조절하거나 직접 입력 후 <strong>[다음]</strong> 클릭.</li>
            </ul>
        </div>
    </div>

    <!-- Page 3: Hard Disk and Network Configuration -->
    <div class="page-block" id="page-3">
        <h2 class="section-title">3. 가상 하드 디스크 연결 및 네트워크 격리</h2>

        <div class="image-placeholder">
            <span>[스냅샷 삽입: 버추얼박스 기존 가상 하드 디스크 파일(.vmdk) 연결 화면]</span>
            <span class="text-sm text-slate-400 mt-2 font-normal">이곳에 다운로드 받은 vmdk 파일을 추가하는 캡처 이미지를 삽입하세요.</span>
        </div>
        <div class="source-link">
            캡처 참조 출처: <a href="https://www.virtualbox.org/manual/ch05.html#vdis" target="_blank" rel="noopener noreferrer">VirtualBox 공식 매뉴얼 - 가상 스토리지 설정</a>
        </div>

        <div class="content-block">
            <span class="step-title">Step 3-1. 하드 디스크 설정</span><br>
            이 단계가 가장 중요합니다. 새 하드 디스크를 만드는 것이 아니라 다운로드한 이미지를 마운트(Mount, 시스템에 연결)해야 합니다.
            <ol class="list-decimal ml-8 mt-2 space-y-2">
                <li>하드 디스크 설정 화면에서 <strong>[기존 가상 하드 디스크 파일 사용]</strong> 라디오 버튼을 선택합니다.</li>
                <li>드롭다운 메뉴 우측에 있는 <strong>[폴더 아이콘(가상 광디스크 파일 선택)]</strong>을 클릭합니다.</li>
                <li>새 창이 뜨면 <strong>[추가(A)]</strong> 버튼을 클릭합니다.</li>
                <li>앞서 압축을 해제했던 폴더(예: <code>C:\VMs\Metasploitable2</code>)로 이동하여 <code>Metasploitable.vmdk</code> 파일을 선택하고 <strong>[열기]</strong>를 누릅니다.</li>
                <li>목록에서 해당 파일이 선택된 것을 확인하고 <strong>[선택]</strong> 버튼을 누릅니다.</li>
                <li>마지막으로 <strong>[만들기]</strong> 버튼을 클릭하여 VM 생성을 완료합니다.</li>
            </ol>
        </div>

        <div class="image-placeholder">
            <span>[스냅샷 삽입: 버추얼박스 네트워크 설정 - '호스트 전용 어댑터' 변경 화면]</span>
            <span class="text-sm text-slate-400 mt-2 font-normal">이곳에 네트워크 어댑터 격리 설정 캡처 이미지를 삽입하세요.</span>
        </div>
        <div class="source-link">
            캡처 참조 출처: <a href="https://www.virtualbox.org/manual/ch06.html#network_hostonly" target="_blank" rel="noopener noreferrer">VirtualBox 공식 매뉴얼 - 호스트 전용 네트워킹</a>
        </div>

        <div class="content-block">
            <span class="step-title">Step 3-2. 네트워크 설정 변경 (필수 보안 조치)</span><br>
            가상 머신이 생성되었지만 아직 실행하면 안 됩니다. 네트워크 설정을 변경하여 샌드박스(Sandbox, 외부와 격리된 안전한 실행 환경)를 완성해야 합니다.
            <ol class="list-decimal ml-8 mt-2 space-y-2">
                <li>버추얼박스 관리자 목록에서 생성한 <code>Metasploitable2</code>를 한 번 클릭하여 선택합니다.</li>
                <li>상단의 <strong>[설정(S)]</strong> 톱니바퀴 아이콘을 클릭합니다.</li>
                <li>좌측 메뉴에서 <strong>[네트워크]</strong> 탭을 선택합니다.</li>
                <li>어댑터 1 탭에서 '다음에 연결됨' 항목을 기본값인 <code>NAT</code>에서 <strong><code>호스트 전용 어댑터</code></strong> (Host-Only Adapter)로 변경합니다.</li>
                <li>이름 항목에 <code>VirtualBox Host-Only Ethernet Adapter</code>가 정상적으로 선택되었는지 확인 후 <strong>[확인]</strong> 버튼을 누릅니다.</li>
            </ol>
        </div>

        <div class="explanation-box">
            <strong>용어 해설: NAT vs 호스트 전용 어댑터</strong><br>
            NAT (Network Address Translation, 네트워크 주소 변환) 방식은 가상 머신이 호스트 PC를 통해 외부 인터넷으로 나갈 수 있게 해줍니다. 
            반면, 호스트 전용 어댑터는 가상 머신과 호스트 PC(현재 사용 중인 내 컴퓨터) 사이에서만 통신이 가능한 폐쇄망을 구축합니다. 
            취약한 실습용 서버가 외부 해커의 표적이 되지 않도록 물리적으로 차단하는 가장 확실한 아키텍처 설계입니다.
        </div>
    </div>

    <!-- Page 4: Booting and Verification -->
    <div class="page-block" id="page-4">
        <h2 class="section-title">4. 가상 머신 실행 및 초기 접속 확인</h2>

        <div class="image-placeholder">
            <span>[스냅샷 삽입: 메타스플로잇터블2 부팅 완료 및 msfadmin 로그인 프롬프트 화면]</span>
            <span class="text-sm text-slate-400 mt-2 font-normal">이곳에 부팅이 완료된 CLI 터미널 캡처 이미지를 삽입하세요.</span>
        </div>
        <div class="source-link">
            캡처 참조 출처: <a href="https://docs.rapid7.com/metasploit/metasploitable-2-exploitability-guide/" target="_blank" rel="noopener noreferrer">Rapid7 공식 문서 - Metasploitable 2 가이드</a>
        </div>

        <div class="content-block">
            <span class="step-title">Step 4-1. 가상 머신 부팅</span><br>
            모든 설정이 완료되었습니다. 버추얼박스 관리자 화면에서 <code>Metasploitable2</code>를 선택하고 상단의 초록색 화살표 <strong>[시작(T)]</strong> 버튼을 클릭합니다.
            검은 화면에 다양한 부팅 로그가 올라가며 리눅스가 시작됩니다.
        </div>

        <div class="content-block">
            <span class="step-title">Step 4-2. 시스템 로그인</span><br>
            부팅이 완료되면 화면 맨 아래에 <code>metasploitable login:</code> 이라는 프롬프트(Prompt, 입력 대기 표시)가 나타납니다. 
            초기 접속 계정 정보는 다음과 같습니다. (커서를 화면 안으로 클릭하여 입력 모드로 전환하세요.)
            <ul class="list-disc ml-8 mt-2 space-y-2">
                <li><strong>아이디 (login):</strong> <code>msfadmin</code></li>
                <li><strong>비밀번호 (Password):</strong> <code>msfadmin</code> <span class="highlight">(비밀번호 입력 시 화면에는 아무 글자도 표시되지 않으나 정상 입력 중이니 타이핑 후 엔터를 누르세요.)</span></li>
            </ul>
        </div>

        <div class="tip-box">
            <strong>자주 오해하는 부분 (Common Mistakes)</strong><br>
            리눅스 환경에서는 보안상 패스워드를 입력할 때 화면에 <code>***</code> 표시는 물론 커서의 이동조차 보이지 않습니다. 
            키보드가 고장 나거나 시스템이 멈춘 것이 아니므로 당황하지 말고 <code>msfadmin</code>을 타이핑한 후 엔터키를 누르시면 됩니다. 
            가상 머신에서 마우스 커서를 호스트 PC로 다시 빼내려면 키보드 우측의 <code>Ctrl</code> 키 (호스트 키)를 누르세요.
        </div>

        <div class="content-block">
            <span class="step-title">Step 4-3. IP 주소 확인</span><br>
            로그인에 성공하면 <code>msfadmin@metasploitable:~$</code> 셸(Shell, 명령어 해석기)이 나타납니다. 
            명령어 <code>ifconfig</code> (Interface Configuration, 네트워크 인터페이스 설정)를 입력하고 엔터를 누릅니다.
            출력된 내용 중 <code>eth0</code> 항목의 <code>inet addr:</code> 뒤에 적힌 IP 주소(예: 192.168.56.101)를 메모해 둡니다. 이 IP 주소가 향후 칼리 리눅스(Kali Linux)에서 공격을 수행할 타겟 서버의 주소가 됩니다.
        </div>
    </div>

</div>

<!-- 스크롤 위치 저장 및 복구 스크립트 -->
<script>
    document.addEventListener("DOMContentLoaded", function() {
        // 세션 스토리지에서 이전 스크롤 위치를 가져와서 복원
        const savedScrollPosition = sessionStorage.getItem("textbookScrollPosition");
        if (savedScrollPosition) {
            window.scrollTo({
                top: parseInt(savedScrollPosition, 10),
                behavior: "instant"
            });
        }

        // 스크롤 시점마다 위치를 세션 스토리지에 저장 (새로고침 시 유지하기 위함)
        let scrollTimeout;
        window.addEventListener("scroll", function() {
            if (scrollTimeout) {
                clearTimeout(scrollTimeout);
            }
            scrollTimeout = setTimeout(function() {
                sessionStorage.setItem("textbookScrollPosition", window.scrollY);
            }, 100);
        });
    });
</script>

</body>
</html>
