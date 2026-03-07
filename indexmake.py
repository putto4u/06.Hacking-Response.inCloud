import os
from datetime import datetime
from collections import defaultdict

# 설정: 제외할 파일명, 폴더 및 허용할 확장자
EXCLUDE_FILES = ['index.html', 'generate_index.py', '.DS_Store']
EXCLUDE_DIRS = ['.git', '.github', '__pycache__']
ALLOWED_EXTENSIONS = ('.html', '.md')

def get_folder_icon(folder_name):
    """
    폴더명에 포함된 키워드를 분석하여 적절한 보안/인프라 아이콘을 반환합니다.
    """
    name_lower = folder_name.lower()
    if '루트' in name_lower or folder_name == '.':
        return 'fa-network-wired'
    elif 'aws' in name_lower or 'cloud' in name_lower:
        return 'fa-brands fa-aws'
    elif 'iam' in name_lower or '접근' in name_lower or '비인가' in name_lower:
        return 'fa-user-lock'
    elif '방화벽' in name_lower or 'ngfw' in name_lower or 'snort' in name_lower or '네트워크' in name_lower:
        return 'fa-route'
    elif '취약점' in name_lower or 'owasp' in name_lower or '공격' in name_lower or '해킹' in name_lower:
        return 'fa-biohazard text-red-500' # 특별히 위험/보안 관련 폴더는 붉은색 강조
    elif 'db' in name_lower or '데이터' in name_lower:
        return 'fa-database'
    else:
        return 'fa-folder-open'

def get_file_icon(file_name):
    """
    파일명에 포함된 키워드 및 확장자를 분석하여 파일 아이콘을 반환합니다.
    """
    name_lower = file_name.lower()
    if name_lower.endswith('.md'):
        return 'fa-file-lines'
    elif '보안' in name_lower or '가이드' in name_lower or '취약점' in name_lower:
        return 'fa-file-shield text-red-400'
    else:
        return 'fa-file-code'

def create_index_html():
    # 디렉토리별로 파일을 그룹화하기 위한 딕셔너리 생성
    # 구조: {'폴더명': [{'name': '파일명', 'path': '상대경로', 'mtime': 수정시간, 'name_without_ext': '확장자제외명'}, ...]}
    grouped_files = defaultdict(list)
    
    for root, dirs, files in os.walk("."):
        # 제외할 폴더 필터링
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # 현재 폴더명 결정 (최상위는 '루트 디렉터리'로 표기)
        folder_name = "루트 디렉터리" if root == "." else os.path.basename(root)
        
        for file in files:
            if file.endswith(ALLOWED_EXTENSIONS) and file not in EXCLUDE_FILES:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, ".")
                web_path = relative_path.replace(os.sep, '/')
                name_without_ext = os.path.splitext(file)[0]
                
                grouped_files[folder_name].append({
                    'path': web_path,
                    'name': file,
                    'name_without_ext': name_without_ext,
                    'mtime': os.path.getmtime(full_path)
                })

    # 폴더 이름순 정렬 (루트 디렉터리를 가장 위로)
    sorted_folders = sorted(grouped_files.keys(), key=lambda x: (x != "루트 디렉터리", x))
    
    # 생성 시간 기록
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M KST')

    # HTML 템플릿 상단 작성 (SecOps 다크 모드 테마 적용)
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Putto's SecOps - 클라우드 보안 및 모의 해킹 아카이브</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Fira+Code:wght@400;500&display=swap');
        
        body {{ 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: #0f172a; 
            color: #cbd5e1; 
        }}
        .font-mono {{ font-family: 'Fira Code', monospace; }}
        
        .cyber-header {{
            background: radial-gradient(circle at 50% 0%, #134e4a 0%, #0f172a 70%);
            border-bottom: 1px solid rgba(16, 185, 129, 0.2);
        }}
        
        .cyber-card {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
        }}
        
        .cyber-card:hover {{
            transform: translateY(-4px);
            border-color: #10b981;
            box-shadow: 0 0 20px -5px rgba(16, 185, 129, 0.4);
        }}

        .cyber-badge {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
        }}

        .alert-banner {{
            background: linear-gradient(90deg, rgba(127, 29, 29, 0.9) 0%, rgba(153, 27, 27, 0.9) 100%);
            border-left: 4px solid #ef4444;
        }}

        .scanlines {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0.1));
            background-size: 100% 4px;
            pointer-events: none;
            z-index: 50;
            opacity: 0.3;
        }}
    </style>
</head>
<body class="antialiased selection:bg-emerald-500 selection:text-slate-900 relative">
    <div class="scanlines"></div>

    <!-- Alert Banner (Cost Warning) -->
    <div class="alert-banner text-white px-6 py-3 shadow-md relative z-40">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <div class="flex items-center space-x-3 text-sm">
                <i class="fas fa-triangle-exclamation text-red-300 animate-pulse text-lg"></i>
                <span class="font-medium tracking-wide">
                    <strong class="text-red-200">Billing Alert:</strong> 본 과정의 실습 중 
                    <span class="font-mono bg-red-950/50 px-1 py-0.5 rounded text-red-100">AWS Network Firewall</span>, 
                    <span class="font-mono bg-red-950/50 px-1 py-0.5 rounded text-red-100">NAT Gateway</span>, 
                    <span class="font-mono bg-red-950/50 px-1 py-0.5 rounded text-red-100">EKS Control Plane</span> 등은 대기 상태에서도 <strong>시간당 고정 비용이 발생</strong>하므로 실습 종료 후 즉시 리소스를 파기(Destroy)해야 합니다.
                </span>
            </div>
        </div>
    </div>

    <header class="cyber-header py-16 px-6 shadow-2xl relative z-30">
        <div class="max-w-6xl mx-auto">
            <div class="flex items-center space-x-5 mb-6">
                <div class="bg-slate-900 p-4 rounded-xl border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                    <i class="fas fa-shield-halved text-4xl text-emerald-400"></i>
                </div>
                <div>
                    <h1 class="text-4xl md:text-5xl font-black tracking-tight text-white mb-2">
                        Putto's SecOps <span class="text-emerald-400 font-light">&</span> Pen-Testing
                    </h1>
                    <p class="text-emerald-500/80 font-mono text-sm tracking-widest uppercase">Cloud Security Architecture & Offensive Strategies</p>
                </div>
            </div>
            
            <p class="text-slate-400 text-lg max-w-3xl leading-relaxed mb-6">
                엔터프라이즈 클라우드 인프라 방어 체계 구축 및 모의 해킹(Penetration Testing, 시스템의 취약점을 찾기 위해 합법적으로 시도하는 공격) 실무 교육 아카이브입니다. IAM(Identity and Access Management, 자격 증명 및 접근 관리) 기반의 제로 트러스트(Zero Trust) 설계부터 인프라 애즈 코드(IaC, 코드형 인프라)를 활용한 자동화된 보안 배포까지 다룹니다.
            </p>

            <div class="flex items-center text-sm font-mono text-slate-500 bg-slate-900/50 w-max px-4 py-2 rounded-lg border border-slate-800">
                <i class="fas fa-terminal mr-3 text-emerald-500"></i>
                <span>Last Compiled: <span class="text-slate-300">{current_time}</span></span>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 py-12 relative z-30">
"""

    # 그룹화된 폴더 및 파일 리스트를 HTML 섹션으로 동적 생성
    for folder in sorted_folders:
        files = grouped_files[folder]
        # 파일명 기준 오름차순 정렬
        files.sort(key=lambda x: x['name'])
        
        folder_icon = get_folder_icon(folder)
        
        # 특정 보안 관련 폴더는 테두리 및 아이콘 색상을 붉은색으로 강조 처리
        section_border_color = "border-red-900/50" if "fa-biohazard" in folder_icon else "border-slate-800"
        icon_color = "text-red-500" if "fa-biohazard" in folder_icon else "text-emerald-500"
        badge_style = "bg-red-900/30 border-red-500/50 text-red-400" if "fa-biohazard" in folder_icon else "cyber-badge"

        html_content += f"""
        <!-- Section: {folder} -->
        <section class="mb-14">
            <div class="flex items-center space-x-3 mb-6 border-b {section_border_color} pb-3">
                <i class="fas {folder_icon} {icon_color}"></i>
                <h2 class="text-2xl font-bold text-slate-100">{folder}</h2>
                <span class="{badge_style} text-xs font-mono px-2.5 py-1 rounded-md">{len(files)} File(s)</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
"""
        
        for file in files:
            file_icon = get_file_icon(file['name'])
            # 카드 hover 시 효과 (보안 카드는 붉은색, 일반은 에메랄드색)
            hover_border = "group-hover:border-red-500/50 group-hover:text-red-500" if "text-red" in file_icon else "group-hover:border-emerald-500/50"
            title_hover = "group-hover:text-red-400" if "text-red" in file_icon else "group-hover:text-emerald-400"

            html_content += f"""
                <a href="{file['path']}" target="_blank" class="cyber-card p-5 rounded-xl border border-slate-700 shadow-lg flex items-start space-x-4 group">
                    <div class="bg-slate-900 p-3 rounded-lg text-slate-400 border border-slate-700 transition-colors {hover_border}">
                        <i class="fas {file_icon.replace(' text-red-400', '')} text-xl"></i>
                    </div>
                    <div class="overflow-hidden w-full">
                        <h3 class="font-bold text-slate-200 truncate transition-colors {title_hover}" title="{file['name_without_ext']}">{file['name_without_ext']}</h3>
                        <p class="text-xs text-slate-500 mt-1 truncate font-mono">{file['name']}</p>
                    </div>
                </a>"""
        
        html_content += """
            </div>
"""
        # 120번 섹션 등 보안 정책/솔루션 관련 컨텍스트 박스 추가 처리
        if "120." in folder or "보안정책" in folder:
             html_content += """
            <div class="mt-6 p-4 bg-slate-800/50 border-l-2 border-red-500 rounded-r text-sm text-slate-400">
                <strong>아키텍처 참고(Architecture Note):</strong> WAF(Web Application Firewall, 웹 애플리케이션 방화벽) 및 IPS(Intrusion Prevention System, 침입 방지 시스템) 구성 시 트래픽 검사 경로에 따른 병목(Bottleneck) 현상을 고려하여 설계해야 합니다.
            </div>"""

        html_content += """
        </section>"""

    # HTML 템플릿 하단 작성
    html_content += """
    </main>

    <footer class="border-t border-slate-800 py-10 text-center relative z-30 bg-slate-900">
        <div class="max-w-6xl mx-auto px-6 flex flex-col items-center">
            <div class="flex space-x-4 mb-4 text-emerald-500 text-xl">
                <i class="fa-brands fa-aws hover:text-white transition-colors cursor-pointer"></i>
                <i class="fa-brands fa-github hover:text-white transition-colors cursor-pointer"></i>
                <i class="fa-brands fa-linux hover:text-white transition-colors cursor-pointer"></i>
            </div>
            <p class="text-slate-500 text-sm font-mono">&copy; 2026 Putto's SecOps Architecture Training. All rights reserved.</p>
            <p class="text-slate-600 text-xs mt-2">Zero Trust & Offensive Security Focused</p>
        </div>
    </footer>
</body>
</html>
"""

    # 파일 쓰기
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    total_files = sum(len(v) for v in grouped_files.values())
    print(f"성공: {total_files}개의 보안/인프라 실습 파일을 포함한 index.html이 생성되었습니다.")

if __name__ == "__main__":
    create_index_html()
