import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {ifrsCatalog,applyCatalog} from '../app/servicos/ifrs.js';
import {officialSubjects,confirmedSubjectIds,thematicSummary,subjectFrequency,setQuestionSubjects} from '../app/servicos/tematica.js';
import {filteredQuestions,validate,merge} from '../app/servicos/model.js';
const catalog=ifrsCatalog(JSON.parse(readFileSync(new URL('../dados/fontes/IFRS_Matematica_Questoes_2016_2026.json',import.meta.url))));
const [a,b,c]=officialSubjects(catalog).map(x=>x.id);
const q1='IFRS-2016-1-Q01',q2='IFRS-2016-1-Q02';
function classified(){return setQuestionSubjects(setQuestionSubjects(catalog,q1,[a,b]),q2,[a]);}
test('31 assuntos oficiais existentes, sem criação e sem inferência por nome',()=>{
 assert.equal(officialSubjects(catalog).length,31);assert.equal(catalog.questions.length,180);assert.deepEqual(thematicSummary(catalog),{total:180,confirmed:0,pending:180});
 assert.ok(catalog.questions.every(q=>q.assuntoIds.length===0));assert.equal(subjectFrequency(catalog).length,31);
});
test('múltiplos vínculos e consulta do segundo assunto, sem mutar o estado anterior',()=>{
 const original=structuredClone(catalog);const s=classified();assert.deepEqual(catalog,original);
 assert.equal(s.subjects.length,catalog.subjects.length);assert.deepEqual(filteredQuestions(s,{subjectId:b}).map(q=>q.id),[q1]);assert.equal(filteredQuestions(s,{subjectId:a}).length,2);
 assert.deepEqual(thematicSummary(s),{total:180,confirmed:2,pending:178});
});
test('conta uma vez por assunto mesmo com IDs repetidos e percentuais podem exceder 100%',()=>{
 const s=classified();s.questions[0].assuntoIds=[a,b,a,b];validate(s);
 const counts=subjectFrequency(s,{year:'2016',semester:'1'});assert.equal(counts.find(x=>x.id===a).count,2);assert.equal(counts.find(x=>x.id===b).count,1);assert.equal(counts.find(x=>x.id===a).percentage,20);
 const onlyOne=subjectFrequency(s,{subjectId:b});assert.equal(onlyOne.reduce((sum,x)=>sum+x.percentage,0),200);
 assert.deepEqual(confirmedSubjectIds(s,s.questions[0]),[a,b]);
});
test('denominador respeita ano, semestre, disciplina e todos os filtros ativos',()=>{
 const s=classified();assert.ok(subjectFrequency(s,{year:'2016',semester:'1',disciplineId:'matematica'}).every(x=>x.total===10));
 assert.ok(subjectFrequency(s,{year:'2016',semester:'2'}).every(x=>x.total===10&&x.count===0&&x.pending===10));
 assert.deepEqual(subjectFrequency(s,{disciplineId:'outra'}),[]);
 assert.ok(subjectFrequency(s,{year:'1900'}).every(x=>x.total===0&&x.percentage===0&&x.pending===0));
});
test('zero confirmado difere de pendência e permite remover ou revisar associações',()=>{
 let s=classified();const zero=subjectFrequency(s).find(x=>x.id===c);assert.equal(zero.count,0);assert.equal(zero.pending,178);
 s=setQuestionSubjects(s,q1,[],'Ainda pendente de conferência.');assert.equal(thematicSummary(s).confirmed,1);assert.equal(filteredQuestions(s,{subjectId:b}).length,0);assert.equal(s.questions[0].assuntosObservacao,'Ainda pendente de conferência.');
 s=setQuestionSubjects(s,q1,[c,c]);assert.deepEqual(s.questions[0].assuntoIds,[c]);assert.ok(Number.isFinite(Date.parse(s.questions[0].assuntosRevisadosEm)));
});
test('vínculos inválidos, grupos históricos e disciplinas diferentes são rejeitados',()=>{
 for(const ids of [['inexistente'],[catalog.subjects.find(s=>s.kind==='editalGroup').id],[''],[null]])assert.throws(()=>setQuestionSubjects(catalog,q1,ids));
 assert.throws(()=>setQuestionSubjects(catalog,'inexistente',[a]));assert.throws(()=>setQuestionSubjects(catalog,q1,'texto'));
 const s=structuredClone(catalog);s.subjects.find(x=>x.id===a).disciplineId='outra';s.disciplines.push({id:'outra',name:'Outra'});assert.throws(()=>setQuestionSubjects(s,q1,[a]));
});
test('reimportação e backup não apagam associações nem alteram classificação original',()=>{
 const s=classified();const updated=setQuestionSubjects(s,q1,[a,b],'Conferência manual de teste.');const q=updated.questions[0];
 for(const key of Object.keys(catalog.questions[0]).filter(k=>k!=='assuntoIds'))assert.deepEqual(q[key],catalog.questions[0][key]);
 assert.deepEqual(applyCatalog(updated,catalog),updated);assert.deepEqual(merge(updated,catalog),updated);assert.equal(JSON.stringify(validate(JSON.parse(JSON.stringify(updated)))),JSON.stringify(updated));
});
test('estado anterior sem assuntoIds é aceito e não reescrito na leitura',()=>{
 const old=structuredClone(catalog);old.questions.forEach(q=>delete q.assuntoIds);const before=structuredClone(old);validate(old);thematicSummary(old);subjectFrequency(old);assert.deepEqual(old,before);assert.equal(thematicSummary(old).pending,180);
 const migrated=applyCatalog(old,catalog);assert.deepEqual(migrated.questions,old.questions.map(q=>({...q,assuntoIds:[]})));assert.deepEqual(old,before);
});
