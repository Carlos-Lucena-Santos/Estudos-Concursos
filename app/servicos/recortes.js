// Metadados de apresentação ficam fora do IndexedDB: não reclassificam questões.
export async function loadClippings(){
 const response=await fetch(new URL('../../dados/questoes/recortes-completos.json',import.meta.url));
 if(!response.ok)throw Error(`Recortes indisponíveis (${response.status}).`);
 const metadata=await response.json();
 if(metadata.version!==1||!Array.isArray(metadata.questions))throw Error('Metadados de recorte inválidos.');
 return new Map(metadata.questions.map(item=>[item.id,item]));
}
export function clippingURL(path){
 if(typeof path!=='string'||!/^dados\/(provas|questoes\/imagens)\/[A-Za-z0-9_./-]+$/.test(path)||path.split('/').includes('..'))throw Error('Caminho de recorte inválido.');
 return new URL(`../../${path}`,import.meta.url).href;
}
