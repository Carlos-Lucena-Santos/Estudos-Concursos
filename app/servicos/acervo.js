// Projeção de consulta: a classificação preparada prevalece na apresentação,
// sem alterar revisões pessoais, backups ou outras coleções do navegador.
export function classifiedCollection(personal, catalog) {
 const references=new Map((catalog?.questions||[]).map(q=>[q.id,q]));
 return {...personal,questions:personal.questions.map(q=>{
  const reference=references.get(q.id);
  if(!reference)return q;
  return {...q,assuntoIds:[...new Set(reference.assuntoIds||[])],
   classificacaoPublicaJustificativa:reference.classificacaoPublicaJustificativa};
 })};
}
