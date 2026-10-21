import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url);
const meta=JSON.parse(readFileSync(new URL('dados/questoes/IFRS-2016-1-recortes.json',root)));
const source=JSON.parse(readFileSync(new URL('dados/fontes/IFRS_Matematica_Questoes_2016_2026.json',root)));
const review=JSON.parse(readFileSync(new URL('dados/questoes/IFRS-2016-1-verificacao.json',root)));
const sha=buffer=>createHash('sha256').update(buffer).digest('hex');
test('dez recortes correspondem aos IDs e páginas da base V0.2',()=>{
 assert.equal(meta.questions.length,10);assert.equal(new Set(meta.questions.map(q=>q.id)).size,10);
 for(let i=1;i<=10;i++){const id=`IFRS-2016-1-Q${String(i).padStart(2,'0')}`;const crop=meta.questions.find(q=>q.id===id);const original=source.classificacoes.find(q=>q.ID===id);assert.ok(crop);assert.equal(crop.page,original['Página PDF']);assert.equal(crop.parts.length,1);assert.equal(crop.possibleContinuation,false);}
});
test('PNG íntegro e status ok vinculado à inspeção do arquivo exato',()=>{
 assert.equal(sha(readFileSync(new URL(meta.pdf,root))),meta.pdfSha256);assert.equal(review.pdfSha256,meta.pdfSha256);
 for(const crop of meta.questions){const png=readFileSync(new URL(crop.image,root));assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.equal(png.readUInt32BE(16),crop.width);assert.equal(png.readUInt32BE(20),crop.height);assert.ok(crop.width>=900);assert.equal(crop.imageSha256,sha(png));assert.equal(crop.status,'ok');assert.equal(review.questions[crop.id].checked,true);assert.equal(review.questions[crop.id].imageSha256,crop.imageSha256);assert.equal(crop.warnings.length,0);}
});
