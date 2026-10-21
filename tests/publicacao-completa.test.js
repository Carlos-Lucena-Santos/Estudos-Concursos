import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {ifrsCatalog,applyCatalog} from '../app/servicos/ifrs.js';
import {attachPublicClassification} from '../app/servicos/classificacao-publica.js';
import {officialSubjects,setQuestionSubjects,subjectFrequency,thematicSummary} from '../app/servicos/tematica.js';
const root=new URL('../',import.meta.url);
const read=path=>JSON.parse(readFileSync(new URL(path,root)));
const original=read('dados/fontes/IFRS_Matematica_Questoes_2016_2026.json');
const raw=ifrsCatalog(original),layer=read('dados/questoes/classificacao-confirmada.json'),crops=read('dados/questoes/recortes-completos.json');
const catalog=attachPublicClassification(raw,layer);
const sha=file=>createHash('sha256').update(readFileSync(new URL(file,root))).digest('hex');
test('180 classificações com justificativa e apenas os 31 assuntos existentes',()=>{
 assert.deepEqual(thematicSummary(catalog),{total:180,confirmed:180,pending:0});
 assert.equal(officialSubjects(catalog).length,31);assert.equal(catalog.subjects.length,raw.subjects.length);
 assert.equal(new Set(layer.questions.map(q=>q.id)).size,180);
 for(const q of catalog.questions){assert.ok(q.assuntoIds.length);assert.equal(q.assuntoIds.length,new Set(q.assuntoIds).size);assert.ok(q.classificacaoPublicaJustificativa.length>15);assert.deepEqual(q.original,original.classificacoes.find(r=>r.ID===q.id));}
});
test('frequências independentes conferem com a matriz editorial e filtros por todas as provas',()=>{
 for(const [year,semester] of [...new Set(catalog.questions.map(q=>`${q.year}/${q.semester}`))].map(p=>p.split('/'))){
  const selected=catalog.questions.filter(q=>String(q.year)===year&&String(q.semester)===semester);assert.equal(selected.length,10);
  for(const row of subjectFrequency(catalog,{year,semester,disciplineId:'matematica'})){
   const expected=layer.questions.filter(q=>selected.some(s=>s.id===q.id)&&new Set(q.assuntoIds).has(row.id)).length;
   assert.equal(row.count,expected);assert.equal(row.percentage,expected*10);
  }
 }
});
test('camada nova preenche pendência antiga, mas preserva revisão pessoal explícita inclusive vazia',()=>{
 const old=structuredClone(raw);old.notes=[{id:'n',subjectId:raw.subjects[0].id,title:'Privado',body:'Preservar'}];const before=structuredClone(old);
 const next=applyCatalog(old,catalog);assert.deepEqual(old,before);assert.equal(thematicSummary(next).confirmed,180);assert.deepEqual(next.notes,old.notes);
 const cleared=setQuestionSubjects(next,next.questions[0].id,[],'Revisão pessoal pendente.');const refreshed=applyCatalog(cleared,catalog);
 assert.equal(thematicSummary(refreshed).pending,1);assert.deepEqual(refreshed.questions[0].assuntoIds,[]);assert.deepEqual(refreshed.notes,old.notes);
 const manuallyImported=structuredClone(raw);manuallyImported.questions[0].assuntoIds=[officialSubjects(raw)[0].id];assert.deepEqual(applyCatalog(manuallyImported,catalog).questions[0].assuntoIds,manuallyImported.questions[0].assuntoIds);
});
test('18 PDFs e 180 imagens ligadas aos IDs, hashes e dimensões consistentes',()=>{
 assert.equal(crops.questions.length,180);assert.equal(new Set(crops.questions.map(q=>q.pdf)).size,18);
 for(const q of crops.questions){assert.ok(catalog.questions.some(x=>x.id===q.id));assert.equal(sha(q.pdf),q.pdfSha256);assert.equal(sha(q.image),q.imageSha256);assert.ok(['ok','revisar'].includes(q.status));const png=readFileSync(new URL(q.image,root));assert.equal(png.readUInt32BE(16),q.width);assert.equal(png.readUInt32BE(20),q.height);assert.ok(q.parts.length>=1);assert.ok(q.text.length>40);assert.equal(q.textStatus,'revisar');}
});
test('classificação editorial inválida ou incompleta é rejeitada',()=>{
 for(const transform of [s=>s.questions.pop(),s=>s.questions.push(s.questions[0]),s=>s.questions[0].assuntoIds=['inexistente']]){const bad=structuredClone(layer);transform(bad);assert.throws(()=>attachPublicClassification(raw,bad));}
});
test('frequência por ano, semestre e assunto confere com conjunto independente, inclusive duplicatas',()=>{
 const state=structuredClone(catalog);
 state.questions[0].assuntoIds.push(state.questions[0].assuntoIds[0]);
 const years=['',...new Set(state.questions.map(q=>String(q.year)))];
 const topics=['',...officialSubjects(state).map(s=>s.id)];
 for(const year of years)for(const semester of ['', '1','2'])for(const subjectId of topics){
  const selected=state.questions.filter(q=>(!year||String(q.year)===year)&&(!semester||String(q.semester)===semester)&&(!subjectId||new Set(q.assuntoIds).has(subjectId)));
  for(const row of subjectFrequency(state,{year,semester,subjectId,disciplineId:'matematica'})){
   const expected=selected.filter(q=>new Set(q.assuntoIds).has(row.id)).length;
   assert.equal(row.total,selected.length);assert.equal(row.count,expected);
   assert.equal(row.percentage,selected.length?100*expected/selected.length:0);
  }
 }
});
