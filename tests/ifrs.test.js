import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {ifrsCatalog,applyCatalog,subjectFrequency} from '../app/servicos/ifrs.js';
import {initial,filteredQuestions,parseCSV} from '../app/servicos/model.js';
const source=JSON.parse(readFileSync(new URL('../dados/fontes/IFRS_Matematica_Questoes_2016_2026.json',import.meta.url),'utf8'));
const catalog=ifrsCatalog(source);
test('180 IDs e campos originais preservados, sem reclassificação',()=>{
 assert.equal(catalog.questions.length,180);assert.equal(new Set(catalog.questions.map(q=>q.id)).size,180);
 source.classificacoes.forEach(r=>{const q=catalog.questions.find(q=>q.id===r.ID);assert.deepEqual(q.original,r);assert.equal(q.page,r['Página PDF']);assert.equal(q.classification,r.Confiança);assert.equal(q.observations,r.Observações);assert.equal(q.source,r['Arquivo PDF']);assert.equal(q.year,r.Ano);assert.equal(q.semester,r.Semestre);assert.equal(q.originalClassification,r['Grupo do edital']);});
 assert.equal(catalog.questions.filter(q=>q.reviewRequired).length,14);
});
test('18 provas com 10 questões; filtros de ano, semestre e grupo',()=>{
 const exams=new Set(catalog.questions.map(q=>q.exam));assert.equal(exams.size,18);
 for(const exam of exams){const [year,semester]=exam.split('/');assert.equal(filteredQuestions(catalog,{year,semester}).length,10);}
 const functions=catalog.subjects.find(s=>s.name==='Funções'&&s.kind==='editalGroup');assert.equal(filteredQuestions(catalog,{subjectId:functions.id}).length,36);
 for(const q of catalog.questions){assert.ok(filteredQuestions(catalog,{subjectId:q.subsubjectId}).some(x=>x.id===q.id));}
});
test('31 tópicos integrais; temas preservados sem inferir vínculo a tópico oficial',()=>{
 assert.equal(catalog.subjects.filter(s=>s.kind==='editalTopic').length,31);
 for(const t of source.conteudo_programatico){const s=catalog.subjects.find(s=>s.kind==='editalTopic'&&s.name===t.topico);assert.ok(s);assert.equal(catalog.subjects.find(p=>p.id===s.parentId).name,t.grupo);}
 for(const q of catalog.questions)assert.equal(catalog.subjects.find(s=>s.id===q.subsubjectId).name,q.theme);
});
test('migração aditiva preserva todas as coleções pessoais e conflitos de IDs',()=>{
 const personal=initial();personal.contests[0].name='Meu concurso';personal.subjects=[{...catalog.subjects[0],status:'concluído'}];personal.questions=[{...catalog.questions[0],pdfUrl:'https://example.org/prova.pdf'}];personal.notes=[{id:'n',subjectId:personal.subjects[0].id,title:'Privado',body:'Minha nota'}];personal.attempts=[{id:'a',questionId:personal.questions[0].id,date:'2026-10-20',status:'revisar'}];personal.events=[{id:'e',date:'2026-10-20',type:'Revisão',questionId:personal.questions[0].id}];
 const before=structuredClone(personal);const next=applyCatalog(personal,catalog);
 assert.deepEqual(personal,before);for(const c of ['notes','attempts','events','attachments'])assert.deepEqual(next[c],before[c]);assert.equal(next.contests[0].name,'Meu concurso');assert.equal(next.subjects[0].status,'concluído');assert.equal(next.questions[0].pdfUrl,'https://example.org/prova.pdf');assert.deepEqual(applyCatalog(next,catalog),next);
});
test('frequência usa 31 assuntos e não confirma temas preliminares automaticamente',()=>{
 const counts=subjectFrequency(catalog);assert.equal(counts.length,31);assert.equal(counts.reduce((a,b)=>a+b.count,0),0);assert.ok(counts.every(x=>x.total===180&&x.pending===180));
 const filtered=subjectFrequency(catalog,{year:'2016',semester:'1'});assert.ok(filtered.every(x=>x.total===10&&x.pending===10));
});
test('CSV fornecido corresponde integralmente ao JSON e não separa vírgulas de assuntos',()=>{
 const rows=parseCSV(readFileSync(new URL('../dados/fontes/IFRS_Matematica_Questoes_2016_2026.csv',import.meta.url),'utf8'));
 assert.equal(rows.length,180);rows.forEach((r,i)=>{for(const k of Object.keys(r))assert.equal(r[k],String(source.classificacoes[i][k]));});
 const converted=ifrsCatalog({...source,classificacoes:rows});assert.deepEqual(converted.questions.map(q=>q.id),catalog.questions.map(q=>q.id));
});
