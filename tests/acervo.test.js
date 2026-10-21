import test from 'node:test';
import assert from 'node:assert/strict';
import {classifiedCollection} from '../app/servicos/acervo.js';
import {subjectFrequency} from '../app/servicos/tematica.js';
const topic={id:'a',name:'Assunto',kind:'editalTopic',disciplineId:'matematica'};
test('consulta editorial preserva revisões privadas e aceita vínculos múltiplos sem duplicação',()=>{
 const personal={subjects:[topic,{...topic,id:'b'}],questions:[{id:'q',disciplineId:'matematica',assuntoIds:[],assuntosRevisadosEm:'2026-10-21',assuntosObservacao:'Privado'}],notes:[{body:'Preservar'}]};
 const catalog={questions:[{id:'q',assuntoIds:['a','a','b']}]},before=structuredClone(personal);
 const view=classifiedCollection(personal,catalog);
 assert.deepEqual(view.questions[0].assuntoIds,['a','b']);
 assert.deepEqual(personal,before);assert.equal(view.notes,personal.notes);
 assert.equal(subjectFrequency(view)[0].count,1);
});
test('novas questões preparadas atualizam frequência sem totais fixos e sem perder questões locais',()=>{
 const state={subjects:[topic],questions:[{id:'q',disciplineId:'matematica',assuntoIds:['a']}]};
 assert.equal(subjectFrequency(classifiedCollection(state,{questions:[]}))[0].count,1);
 state.questions.push({id:'nova',disciplineId:'matematica',assuntoIds:['a']});
 const row=subjectFrequency(classifiedCollection(state,{questions:[]}))[0];
 assert.equal(row.count,2);assert.equal(row.total,2);assert.equal(row.percentage,100);
});
