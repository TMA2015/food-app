from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "site/index.html")
s = path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str):
    global s
    if old not in s:
        raise SystemExit(f"{label} pattern not found")
    s = s.replace(old, new, 1)


# 1) Make soup/canh a first-class group for user-created dishes.
replace_once(
    "['vegetable','Rau / củ'],['rice','Gạo / tinh bột'],['duck','Vịt / ngan']",
    "['vegetable','Rau / củ'],['rice','Gạo / tinh bột'],['soup','Canh / súp'],['duck','Vịt / ngan']",
    "soup group",
)
replace_once(
    "syncCapabilityUi();renderGroupSelect(d?d.group:'other');newGroupRow.className='new-group-row';",
    "syncCapabilityUi();renderGroupSelect(d?d.group:(dfRole.value==='rice'?'rice':dfRole.value==='soup'?'soup':'other'));newGroupRow.className='new-group-row';",
    "openDishForm default group",
)
replace_once(
    "dfRole.onchange=()=>{if(dfRole.value==='rice'){dfStyle.value='rice_family';syncCapabilityUi();renderGroupSelect('rice');dfMethod.value='Khác'}};",
    "dfRole.onchange=()=>{if(dfRole.value==='rice'){dfStyle.value='rice_family';syncCapabilityUi();renderGroupSelect('rice');dfMethod.value='Khác'}else if(dfRole.value==='soup'){dfStyle.value='rice_family';syncCapabilityUi();renderGroupSelect('soup');dfMethod.value='Canh'}else if(['rice','soup'].includes(dfGroup.value)){renderGroupSelect('other')}};",
    "dfRole soup auto group",
)

# 2) Add compact/expand controls and a menu-summary button.
replace_once(
    '<div class="toolbar-actions"><button class="btn secondary" id="regen">↻ Tạo lại bữa chưa khóa</button><button class="btn secondary" id="shoppingBtn">🛒 Danh sách đi chợ ↓</button><span class="status" id="status"></span></div>',
    '<div class="toolbar-actions"><button class="btn secondary" id="togglePlanBody">Thu gọn thực đơn ↑</button><button class="btn secondary" id="menuShareBtn">▦ Bản thực đơn</button><button class="btn secondary" id="regen">↻ Tạo lại bữa chưa khóa</button><button class="btn secondary" id="shoppingBtn">🛒 Danh sách đi chợ ↓</button><span class="status" id="status"></span></div>',
    "planner toolbar",
)
replace_once(
    "const planKey='food-app:weekly-plan:preview-v2';let household={adults:2,children:1},slots={},plan=null,savedPlan=null,dirty=false,selector=null,plannerCategories=['all'];",
    "const planKey='food-app:weekly-plan:preview-v2';let household={adults:2,children:1},slots={},plan=null,savedPlan=null,dirty=false,selector=null,plannerCategories=['all'],planExpanded=true;",
    "planner expanded state",
)
replace_once(
    "document.getElementById('saveNote').textContent=savedPlan?'Bạn có thay đổi chưa lưu.':'Đây là bản nháp. Lưu khi bạn đã ưng ý.';renderShopping()}",
    "document.getElementById('saveNote').textContent=savedPlan?'Bạn có thay đổi chưa lưu.':'Đây là bản nháp. Lưu khi bạn đã ưng ý.';syncPlanCollapse();renderShopping()}",
    "renderPlan collapse sync",
)
replace_once(
    "function inferSelectorCategory(d)",
    "function syncPlanCollapse(){const d=document.getElementById('days'),b=document.querySelector('.planner-bottom-actions'),t=document.getElementById('togglePlanBody');if(d)d.hidden=!planExpanded;if(b)b.hidden=!planExpanded;if(t)t.textContent=planExpanded?'Thu gọn thực đơn ↑':'Mở thực đơn ↓'}document.getElementById('togglePlanBody').onclick=()=>{planExpanded=!planExpanded;syncPlanCollapse()};document.getElementById('menuShareBtn').onclick=()=>openShare('menu');\nfunction inferSelectorCategory(d)",
    "collapse helpers",
)

# 3) Add a final-shopping-summary button to the shopping list.
replace_once(
    '<div class="shopping-head-actions">${removed?`<button class="btn secondary" id="restoreShop">Khôi phục ${removed} mục đã bỏ</button>`:\'\'}<button class="btn secondary" id="clearShop">Bỏ đánh dấu</button></div>',
    '<div class="shopping-head-actions"><button class="btn secondary" id="shoppingShareBtn">▦ Bản danh sách cuối</button>${removed?`<button class="btn secondary" id="restoreShop">Khôi phục ${removed} mục đã bỏ</button>`:\'\'}<button class="btn secondary" id="clearShop">Bỏ đánh dấu</button></div>',
    "shopping final button",
)
replace_once(
    "const restore=document.getElementById('restoreShop');if(restore)restore.onclick=()=>{shopState.removed={};saveShopState();renderShopping()};",
    "const finalBtn=document.getElementById('shoppingShareBtn');if(finalBtn)finalBtn.onclick=()=>openShare('shopping');const restore=document.getElementById('restoreShop');if(restore)restore.onclick=()=>{shopState.removed={};saveShopState();renderShopping()};",
    "shopping final handler",
)

# 4) Generic share/print sheet.
share_markup = '''<div class="share-overlay" id="shareOverlay" aria-hidden="true"><div class="share-panel" role="dialog" aria-modal="true" aria-labelledby="shareTitle"><div class="share-head"><div><span class="eyebrow">Bản cuối để lưu / gửi</span><h2 id="shareTitle">Bản thực đơn</h2><p id="shareSubtitle"></p></div><button class="share-close" id="shareClose" aria-label="Đóng">×</button></div><div class="share-body" id="shareContent"></div><div class="share-actions"><button class="btn secondary" id="sharePrint">🖨 In / Lưu PDF</button><button class="btn secondary" id="sharePng">⬇ Lưu ảnh PNG</button><button class="btn primary" id="shareNative">↗ Chia sẻ</button></div></div></div>\n'''
replace_once('<div class="unsaved" id="unsavedPrompt">', share_markup + '<div class="unsaved" id="unsavedPrompt">', "share markup")

css = r'''
/* v0.10 compact planner + final share sheets */
#days[hidden],.planner-bottom-actions[hidden]{display:none!important}.share-overlay{position:fixed;z-index:120;inset:0;display:none;align-items:center;justify-content:center;padding:24px;background:rgba(31,32,28,.38);backdrop-filter:blur(5px)}.share-overlay.on{display:flex}.share-panel{width:min(1080px,calc(100vw - 32px));max-height:calc(100vh - 32px);display:flex;flex-direction:column;background:#fff;border:1px solid var(--border);border-radius:24px;box-shadow:0 30px 90px rgba(35,37,31,.28);overflow:hidden}.share-head{position:relative;padding:24px 76px 18px 26px;border-bottom:1px solid var(--border)}.share-head h2{margin:3px 0 5px;font:600 30px Lora,Georgia,serif}.share-head p{margin:0;color:var(--muted);font-size:12px}.share-close{position:absolute;top:16px;right:16px;width:42px;height:42px;border:1px solid var(--border);border-radius:12px;background:#fff;font-size:22px;cursor:pointer}.share-body{overflow:auto;padding:22px 26px}.share-table{width:100%;border-collapse:collapse;font-size:13px}.share-table th,.share-table td{padding:12px 13px;border:1px solid var(--border);vertical-align:top;text-align:left;line-height:1.5}.share-table th{background:#f6f4ed;font-size:11px;text-transform:uppercase;letter-spacing:.06em}.share-table .share-day{font-weight:800;white-space:nowrap}.share-table .share-status{white-space:nowrap}.share-actions{display:flex;justify-content:flex-end;gap:10px;flex-wrap:wrap;padding:16px 26px;border-top:1px solid var(--border);background:#fbfaf6}.share-note{margin-top:12px;color:var(--muted);font-size:11px;line-height:1.5}@media(max-width:700px){.share-overlay{align-items:flex-end;padding:0}.share-panel{width:100%;max-height:92vh;border-radius:22px 22px 0 0}.share-head{padding:20px 66px 14px 18px}.share-body{padding:16px 14px}.share-actions{padding:12px 14px;display:grid;grid-template-columns:1fr 1fr}.share-actions .btn:last-child{grid-column:1/-1}.share-table{font-size:11px}.share-table th,.share-table td{padding:8px 7px}.toolbar-actions #togglePlanBody,.toolbar-actions #menuShareBtn{width:100%}}@media print{body *{visibility:hidden!important}#shareOverlay,#shareOverlay *{visibility:visible!important}#shareOverlay{display:block!important;position:absolute!important;inset:0!important;padding:0!important;background:#fff!important}.share-panel{width:100%!important;max-height:none!important;border:0!important;border-radius:0!important;box-shadow:none!important}.share-actions,.share-close{display:none!important}.share-body{overflow:visible!important;padding:10mm!important}.share-head{padding:10mm 10mm 4mm!important}.share-table th{background:#f3f3f3!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''
replace_once('</style>\n</head>', css + '</style>\n</head>', "share css")

share_js = r'''let shareKind='menu';
const shareGroupLabels={protein:'Thịt · cá · đạm',veg:'Rau · củ · nấm',carb:'Gạo · bún · mì',pantry:'Gia vị · sốt',other:'Khác'};
function mealShareText(e){if(!e)return '—';return e.items.map(it=>{let suffix='';if(it.dish.style!=='rice_family'&&it.dish.mode==='both')suffix=it.choice==='outside'?' — Ăn ngoài':' — Tự nấu';else if(it.dish.style!=='rice_family'&&it.dish.mode==='outside')suffix=' — Ăn ngoài';return it.dish.name+suffix}).join('\n')}
function shareModel(kind){if(kind==='menu'){const rows=days.map((day,d)=>{const lunch=plan?.entries.find(e=>e.day===d&&e.meal==='lunch'),dinner=plan?.entries.find(e=>e.day===d&&e.meal==='dinner');return lunch||dinner?[day,mealShareText(lunch),mealShareText(dinner)]:null}).filter(Boolean);return {title:'Thực đơn tuần',subtitle:plan?`${plan.household.adults} người lớn${plan.household.children?` · ${plan.household.children} trẻ em`:''}`:'',headers:['Ngày','Trưa','Tối'],rows,filename:'thuc-don-tuan.png'}}const d=visibleShopData(),rows=d.items.map(x=>[shareGroupLabels[x.group]||'Khác',x.name,shopQty(x.q,x.u),shopState.checked[x.key]?'✓ Đã mua':'□ Chưa mua']);return {title:'Danh sách đi chợ',subtitle:plan?`${plan.household.adults} người lớn${plan.household.children?` · ${plan.household.children} trẻ em`:''}`:'',headers:['Nhóm','Mặt hàng','Số lượng','Trạng thái'],rows,filename:'danh-sach-di-cho.png'}}
function escLines(v){return escapeHtml(v).replace(/\n/g,'<br>')}
function openShare(kind){if(!plan)return;shareKind=kind;const m=shareModel(kind);shareTitle.textContent=m.title;shareSubtitle.textContent=m.subtitle;shareContent.innerHTML=`<table class="share-table"><thead><tr>${m.headers.map(h=>`<th>${escapeHtml(h)}</th>`).join('')}</tr></thead><tbody>${m.rows.map(r=>`<tr>${r.map((c,i)=>`<td class="${i===0?'share-day':''} ${kind==='shopping'&&i===3?'share-status':''}">${escLines(c)}</td>`).join('')}</tr>`).join('')}</tbody></table><div class="share-note">Bản này lấy đúng dữ liệu đang hiển thị trong ứng dụng. Bạn có thể in/lưu PDF, lưu ảnh PNG hoặc chia sẻ trực tiếp trên thiết bị hỗ trợ.</div>`;shareOverlay.className='share-overlay on';shareOverlay.setAttribute('aria-hidden','false')}
function closeShare(){shareOverlay.className='share-overlay';shareOverlay.setAttribute('aria-hidden','true')}
function canvasLines(ctx,text,maxWidth){const out=[];String(text??'').split('\n').forEach(par=>{const words=par.split(/\s+/).filter(Boolean);if(!words.length){out.push('');return}let line='';for(const w of words){const test=line?line+' '+w:w;if(ctx.measureText(test).width>maxWidth&&line){out.push(line);line=w}else line=test}out.push(line)});return out}
function shareCanvas(model){const W=1500,margin=70,tableTop=190,pad=18,lineH=28;const cols=model.headers.length===3?[210,610,610]:[260,570,240,290];const temp=document.createElement('canvas'),ctx=temp.getContext('2d');ctx.font='24px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';const rowLayouts=model.rows.map(r=>{let lines=[],max=1;r.forEach((c,i)=>{const ls=canvasLines(ctx,c,cols[i]-pad*2);lines.push(ls);max=Math.max(max,ls.length)});return {lines,h:max*lineH+pad*2}});const tableH=54+rowLayouts.reduce((a,r)=>a+r.h,0);temp.width=W;temp.height=tableTop+tableH+70;ctx.fillStyle='#ffffff';ctx.fillRect(0,0,temp.width,temp.height);ctx.fillStyle='#1f211d';ctx.font='700 42px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';ctx.fillText(model.title,margin,70);ctx.font='22px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';ctx.fillStyle='#686b63';ctx.fillText(model.subtitle,margin,112);let x=margin,y=tableTop;ctx.font='700 20px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';model.headers.forEach((h,i)=>{ctx.fillStyle='#f1efe8';ctx.fillRect(x,y,cols[i],54);ctx.strokeStyle='#d9d5ca';ctx.strokeRect(x,y,cols[i],54);ctx.fillStyle='#34362f';ctx.fillText(h,x+pad,y+34);x+=cols[i]});y+=54;ctx.font='22px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';rowLayouts.forEach((layout,ri)=>{x=margin;model.rows[ri].forEach((c,i)=>{ctx.fillStyle='#ffffff';ctx.fillRect(x,y,cols[i],layout.h);ctx.strokeStyle='#ddd9cf';ctx.strokeRect(x,y,cols[i],layout.h);ctx.fillStyle='#242620';layout.lines[i].forEach((line,li)=>ctx.fillText(line,x+pad,y+pad+22+li*lineH));x+=cols[i]});y+=layout.h});return temp}
function saveCanvas(canvas,filename,share=false){canvas.toBlob(async blob=>{if(!blob)return;const file=new File([blob],filename,{type:'image/png'});if(share&&navigator.share&&navigator.canShare&&navigator.canShare({files:[file]})){try{await navigator.share({title:shareModel(shareKind).title,files:[file]});return}catch(e){if(e&&e.name==='AbortError')return}}const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1500)},'image/png')}
document.getElementById('shareClose').onclick=closeShare;document.getElementById('shareOverlay').onclick=e=>{if(e.target.id==='shareOverlay')closeShare()};document.getElementById('sharePrint').onclick=()=>window.print();document.getElementById('sharePng').onclick=()=>{const m=shareModel(shareKind);saveCanvas(shareCanvas(m),m.filename,false)};document.getElementById('shareNative').onclick=()=>{const m=shareModel(shareKind);saveCanvas(shareCanvas(m),m.filename,true)};
'''
replace_once("document.getElementById('generate').onclick=", share_js + "document.getElementById('generate').onclick=", "share js")

s = s.replace(
    'Prototype v0.8.1 · Ingredient normalization + recipe data quality',
    'Prototype v0.10 · Compact planner + printable/shareable summaries',
    1,
)

# QA: exact user-facing features must be present in the built page.
checks = [
    "['soup','Canh / súp']",
    "renderGroupSelect('soup')",
    'id="togglePlanBody"',
    'id="menuShareBtn"',
    'id="shoppingShareBtn"',
    'id="shareOverlay"',
    "function openShare(kind)",
    "thuc-don-tuan.png",
    "danh-sach-di-cho.png",
]
for check in checks:
    if check not in s:
        raise SystemExit(f"v0.10 QA missing: {check}")

path.write_text(s, encoding="utf-8")
print(f"v0.10 patch applied: {path} ({len(s)} chars)")
