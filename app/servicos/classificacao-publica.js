import {validate} from './model.js';

// Camada editorial separada das fontes originais e dos vínculos pessoais.
export function attachPublicClassification(catalog, layer) {
 if(layer.version!==1||typeof layer.revision!=='string'||!Array.isArray(layer.questions))throw Error('Classificação pública inválida.');
 const next=structuredClone(catalog),seen=new Set();
 for(const row of layer.questions){
  const q=next.questions.find(q=>q.id===row.id);
  if(!q||seen.has(row.id)||!['confirmada','pendente'].includes(row.status))throw Error('Questão inválida ou duplicada na classificação pública.');
  if(!Array.isArray(row.assuntoIds)||typeof row.justificativa!=='string'||!row.justificativa.trim()||(row.status==='confirmada'&&row.assuntoIds.length===0))throw Error('Classificação sem vínculos ou justificativa válida.');
  seen.add(row.id);
  q.assuntoIds=row.status==='confirmada'?[...new Set(row.assuntoIds)]:[];
  q.classificacaoPublicaVersao=layer.revision;
  q.classificacaoPublicaJustificativa=row.justificativa;
 }
 if(seen.size!==next.questions.length)throw Error('A classificação pública deve cobrir todas as questões do catálogo.');
 return validate(next);
}
