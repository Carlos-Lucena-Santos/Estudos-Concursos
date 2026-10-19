export const collections=['contests','disciplines','subjects','questions','notes','attempts','events','attachments'];
export const uid=()=>crypto.randomUUID();
export function initial(){return {version:1,contests:[{id:'ifrs-2027-1',name:'IFRS • Porto Alegre • Sistemas para Internet • 2027/1',notice:'15/2026',pending:true}],disciplines:[{id:'matematica',name:'Matemática e suas Tecnologias'}],subjects:[],questions:[],notes:[],attempts:[],events:[],attachments:[]};}
export function validate(s){
 if(s?.version!==1)throw Error('Versão de arquivo incompatível.');
 for(const c of collections){if(!Array.isArray(s[c]))throw Error(`Coleção ausente: ${c}`);const ids=new Set();for(const x of s[c]){if(!x||typeof x.id!=='string'||!x.id||ids.has(x.id))throw Error(`ID inválido ou duplicado em ${c}`);ids.add(x.id);}}
 const has=(c,id)=>s[c].some(x=>x.id===id);
 const ref=(c,id)=>{if(id&&!has(c,id))throw Error(`Referência inexistente: ${c}/${id}`);};
 for(const x of s.contests)if(typeof x.name!=='string')throw Error('Concurso sem nome.');
 for(const x of s.disciplines)if(typeof x.name!=='string')throw Error('Disciplina sem nome.');
 for(const x of s.subjects){if(!x.disciplineId)throw Error('Assunto sem disciplina.');if(typeof x.name!=='string')throw Error('Assunto sem nome.');ref('disciplines',x.disciplineId);ref('subjects',x.parentId);for(const id of x.contestIds||[])ref('contests',id);let p=x;const seen=new Set([x.id]);while(p.parentId){if(seen.has(p.parentId))throw Error('Ciclo nos subassuntos.');seen.add(p.parentId);p=s.subjects.find(a=>a.id===p.parentId);}}
 for(const x of s.questions){if(!x.disciplineId||!x.subjectId)throw Error('Questão sem disciplina ou assunto principal.');ref('disciplines',x.disciplineId);ref('subjects',x.subjectId);ref('subjects',x.subsubjectId);for(const id of x.secondaryIds||[])ref('subjects',id);for(const id of x.contestIds||[])ref('contests',id);if(!Number.isInteger(+x.number)||+x.number<1)throw Error('Número de questão inválido.');}
 for(const x of s.notes){if(!x.subjectId)throw Error('Anotação sem assunto.');ref('subjects',x.subjectId);if(typeof x.body!=='string'||typeof x.title!=='string')throw Error('Anotação inválida.');}
 for(const x of [...s.attempts,...s.events]){ref('questions',x.questionId);ref('subjects',x.subjectId);ref('disciplines',x.disciplineId);if(!Number.isFinite(Date.parse(x.date)))throw Error('Data inválida.');}
 for(const x of s.attempts){if(!x.questionId)throw Error('Tentativa sem questão.');} for(const x of s.attempts)if(!['não iniciada','estudando','resolvida','revisar'].includes(x.status))throw Error('Situação inválida.');
 for(const x of s.attachments){if(!x.subjectId)throw Error('Anexo sem assunto.');ref('subjects',x.subjectId);ref('questions',x.questionId);if(typeof x.data!=='string'||!/^data:[^,]*;base64,/.test(x.data)||x.data.length>14000000)throw Error('Anexo inválido ou maior que 10 MB.');}
 return s;
}
export function filteredQuestions(s,f={}){return s.questions.filter(q=>Object.entries(f).every(([k,v])=>!v||(k==='contestId'?(q.contestIds||[]).includes(v):k==='subjectId'?[q.subjectId,...q.secondaryIds||[]].includes(v):k==='status'?(s.attempts.filter(a=>a.questionId===q.id).sort((a,b)=>Date.parse(b.date)-Date.parse(a.date))[0]?.status||'não iniciada')===v:String(q[k]??'')===v)));}
export const chronological=items=>[...items].sort((a,b)=>Date.parse(b.date)-Date.parse(a.date));
export function merge(a,b){validate(b);const out=structuredClone(a);for(const c of collections){const ids=new Set(out[c].map(x=>x.id));out[c].push(...b[c].filter(x=>!ids.has(x.id)));}return validate(out);}
export function parseCSV(text){const rows=[];let row=[],cell='',quoted=false;for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){cell+='"';i++;}else quoted=!quoted;}else if(!quoted&&(c===','||c===';'||c==='\n')){row.push(cell.replace(/\r$/,''));cell='';if(c==='\n'){rows.push(row);row=[];}}else cell+=c;}if(quoted)throw Error('CSV com aspas não fechadas.');if(cell||row.length){row.push(cell.replace(/\r$/,''));rows.push(row);}const [keys,...data]=rows;return data.filter(r=>r.some(Boolean)).map(r=>Object.fromEntries(keys.map((k,i)=>[k.trim(),r[i]||''])));}
