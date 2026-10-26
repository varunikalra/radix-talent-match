import {useEffect,useState} from 'react';
import {FileText,LoaderCircle,RefreshCw,BriefcaseBusiness,GraduationCap,Clock3} from 'lucide-react';
import {Badge,Button,PageHeader,Panel} from '../components/ui';
import {analyzeJD,getJDSample,listJDSamples,JDAnalysis,JDSample} from '../jdApi';

export default function JobIntelligence(){
  const[samples,setSamples]=useState<JDSample[]>([]);
  const[selected,setSelected]=useState('');
  const[text,setText]=useState('');
  const[result,setResult]=useState<JDAnalysis|null>(null);
  const[loading,setLoading]=useState(false);
  const[error,setError]=useState('');

  useEffect(()=>{
    let active=true;
    listJDSamples().then(items=>active&&setSamples(items)).catch(()=>active&&setError('Sample job descriptions could not be loaded. You can still paste custom text.'));
    return ()=>{active=false};
  },[]);

  async function selectSample(id:string){
    setSelected(id);setResult(null);setError('');
    if(!id){setText('');return}
    try{setText((await getJDSample(id)).text)}catch(selectionError){setError(selectionError instanceof Error?selectionError.message:'The sample could not be loaded.')}
  }

  async function analyze(){
    if(!text.trim()){setError('Enter a job description or select a sample first.');return}
    setLoading(true);setError('');setResult(null);
    try{setResult(await analyzeJD(text))}catch(analysisError){setError(analysisError instanceof Error?analysisError.message:'The job description could not be analyzed.')}
    finally{setLoading(false)}
  }

  return <>
    <PageHeader eyebrow="01 / DECODE THE OPPORTUNITY" title="Job Intelligence" description="Understand what the opportunity is really asking for." action={result?<Button variant="secondary" onClick={()=>{setResult(null);setError('')}}><RefreshCw size={15}/>Analyze another</Button>:undefined}/>
    <div className="module-intro"><FileText size={18}/><span>From a job description to a clearer direction.</span><Badge tone="teal">LIVE JD ANALYSIS</Badge></div>
    <div className="two-grid input-grid jd-premium-grid">
      <Panel title="Add a job description" subtitle="Choose a sample or paste the text directly.">
        <label className="field">Sample job
          <select aria-label="Sample job" value={selected} onChange={event=>selectSample(event.target.value)}>
            <option value="">Choose a sample</option>
            {samples.map(sample=><option key={sample.id} value={sample.id}>{sample.name}</option>)}
          </select>
        </label>
        <label className="field">Job description text
          <textarea rows={12} value={text} onChange={event=>{setSelected('');setText(event.target.value)}} placeholder="Paste responsibilities, qualifications and role requirements…"/>
        </label>
        {error&&<p className="field-error" role="alert">{error}</p>}
        <Button onClick={analyze} disabled={loading || !text.trim()}>
          {loading?<><LoaderCircle className="spin" size={16}/>Analyzing requirements</>:<>Analyze job description</>}
        </Button>
      </Panel>

      <Panel title="Extracted intelligence" subtitle="Results are based on this job description only." className="jd-results-panel">
        {loading&&<div className="jd-empty-state"><LoaderCircle className="spin" size={28}/><strong>Reading the role</strong><p>Extracting requirements and RADIX categories…</p></div>}
        {!loading&&!result&&<div className="jd-empty-state"><div className="jd-empty-icon"><FileText size={28}/></div><strong>Ready for a closer look</strong><p>Select a sample or paste text to reveal structured requirements.</p></div>}
        {!loading&&result&&<JDResults result={result}/>} 
      </Panel>
    </div>
  </>
}

function JDResults({result}:{result:JDAnalysis}){
  const categories=result.radix_categories.filter(category=>category.skills.length);
  return <div className="jd-live-results">
    <div className="jd-result-hero">
      <div><BriefcaseBusiness size={18}/><span>Role</span><strong>{result.title||'Not identified'}</strong></div>
      <div><FileText size={18}/><span>Company</span><strong>{result.company||'Not identified'}</strong></div>
    </div>

    <section className="jd-result-section">
      <h3>RADIX skill categories</h3>
      {categories.length?<div className="jd-category-grid">{categories.map(category=><article key={category.code} className="jd-category"><span>{category.code}</span><strong>{category.name}</strong><ul>{category.skills.map(skill=><li key={skill}>{skill}</li>)}</ul></article>)}</div>:<p className="muted">No curated skills were identified.</p>}
    </section>

    <div className="jd-result-columns">
      <section className="jd-result-section"><h3><Clock3 size={16}/>Experience</h3><RequirementList items={result.requirements.experience}/></section>
      <section className="jd-result-section"><h3><GraduationCap size={16}/>Education</h3><RequirementList items={result.requirements.education}/></section>
    </div>

    <section className="jd-result-section"><h3>Responsibilities</h3><RequirementList items={result.responsibilities}/></section>

    {result.unmatched_skills.length>0&&<section className="jd-result-section"><h3>Other detected terms</h3><p className="jd-unmatched">{result.unmatched_skills.join(' · ')}</p></section>}
    <p className="jd-method">Method: {result.extraction_method}</p>
  </div>
}

function RequirementList({items}:{items:string[]}){return items.length?<ul className="jd-requirement-list">{items.map(item=><li key={item}>{item}</li>)}</ul>:<p className="muted">Not identified</p>}
