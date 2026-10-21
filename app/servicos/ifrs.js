import {initial,validate,merge,filteredQuestions} from './model.js';
// IDs derivam do texto da fonte e não da ordem dos registros.
const subjectId=(kind,...parts)=>`ifrs-mat-${kind}-${parts.map(encodeURIComponent).join('/')}`;
export function ifrsCatalog(source){
 if(!Array.isArray(source.classificacoes)||!Array.isArray(source.conteudo_programatico))throw Error('Formato IFRS inválido.');
 const catalog=initial();
 const addSubject=(id,name,parentId,kind,extra={})=>{
  if(!catalog.subjects.some(s=>s.id===id))catalog.subjects.push({id,name,parentId,kind,disciplineId:'matematica',contestIds:['ifrs-2027-1'],status:'não iniciado',...extra});
  return id;
 };
 for(const t of source.conteudo_programatico){
  const group=addSubject(subjectId('grupo',t.grupo),t.grupo,undefined,'editalGroup',{noticeTopic:t.grupo,source:source.referencia});
  addSubject(subjectId('edital',t.grupo,t.topico),t.topico,group,'editalTopic',{noticeTopic:t.topico,source:source.referencia});
 }
 catalog.questions=source.classificacoes.map(r=>{
  const group=subjectId('grupo',r['Grupo do edital']);
  if(!catalog.subjects.some(s=>s.id===group))throw Error(`Grupo não encontrado no edital: ${r['Grupo do edital']}`);
  const theme=addSubject(subjectId('tema',r['Grupo do edital'],r['Assunto específico']),r['Assunto específico'],group,'classificationTheme');
  const secondary=r['Assunto secundário']?[addSubject(subjectId('secundario',r['Assunto secundário']),r['Assunto secundário'],undefined,'classificationTheme')]:[];
  return {id:r.ID,institution:'IFRS',exam:r.Prova,year:r.Ano,semester:r.Semestre,number:r['Questão'],disciplineId:'matematica',subjectId:group,subsubjectId:theme,secondaryIds:secondary,contestIds:['ifrs-2027-1'],theme:r['Assunto específico'],page:r['Página PDF'],source:r['Arquivo PDF'],classification:r.Confiança,originalClassification:r['Grupo do edital'],observations:r.Observações,reviewRequired:r.Confiança==='Revisão necessária',original:structuredClone(r)};
 });
 return validate(catalog);
}
export function applyCatalog(personal,catalog){return merge(personal,catalog);}
export function subjectFrequency(s,filters={}){
 const qs=filteredQuestions(s,filters);
 return s.subjects.filter(x=>x.kind==='editalGroup').map(subject=>({id:subject.id,name:subject.name,count:qs.filter(q=>q.subjectId===subject.id||(q.secondaryIds||[]).includes(subject.id)).length,total:qs.length}));
}
export async function fetchIFRSCatalog(){
 const response=await fetch(new URL('../../dados/fontes/IFRS_Matematica_Questoes_2016_2026.json',import.meta.url));
 if(!response.ok)throw Error(`Não foi possível carregar catálogo IFRS (${response.status}).`);
 return ifrsCatalog(await response.json());
}
