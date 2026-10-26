import {Suspense,lazy,useEffect} from 'react';
import {BrowserRouter,Routes,Route,useLocation} from 'react-router-dom';
import {MotionConfig} from 'motion/react';
import {Toaster} from 'sonner';
import {StoreProvider,useStore} from './store';
import {Action,Empty} from './components/ui';
const Landing=lazy(()=>import('./pages/Landing'));
const Shell=lazy(()=>import('./components/Shell'));
const Overview=lazy(()=>import('./pages/Overview'));
const Intelligence=lazy(()=>import('./pages/Intelligence'));const JobIntelligence=lazy(()=>import('./pages/JobIntelligence'));
const Profile=lazy(()=>import('./pages/Profile'));
const Companies=lazy(()=>import('./pages/Companies'));
const CompanyDetail=lazy(()=>import('./pages/Companies').then(m=>({default:m.CompanyDetail})));
const TalentCheck=lazy(()=>import('./pages/Analysis').then(m=>({default:m.TalentCheck})));
const SkillMatching=lazy(()=>import('./pages/Analysis').then(m=>({default:m.SkillMatching})));
const Roadmap=lazy(()=>import('./pages/Supporting').then(m=>({default:m.Roadmap})));
const History=lazy(()=>import('./pages/Supporting').then(m=>({default:m.History})));
const Settings=lazy(()=>import('./pages/Supporting').then(m=>({default:m.Settings})));
function Scroll(){const{pathname}=useLocation();useEffect(()=>{window.scrollTo(0,0);document.title=pathname==='/'?'RADIX — Your Potential, Decoded.':'RADIX — Talent Intelligence Workspace'},[pathname]);return null}
function Content(){const{state}=useStore();return <MotionConfig reducedMotion={state.reduced?'always':'user'}><Scroll/><Suspense fallback={<div className="skeleton-page" role="status" aria-label="Loading page"><div/><div/><div/><span>Preparing your workspace…</span></div>}><Routes><Route path="/" element={<Landing/>}/><Route path="/workspace" element={<Shell/>}><Route index element={<Overview/>}/><Route path="jobs" element={<JobIntelligence/>}/><Route path="resume" element={<Intelligence resume/>}/><Route path="profile" element={<Profile/>}/><Route path="companies" element={<Companies/>}/><Route path="companies/:companyId" element={<CompanyDetail/>}/><Route path="talent-check" element={<TalentCheck/>}/><Route path="skill-match" element={<SkillMatching/>}/><Route path="insights" element={<Roadmap/>}/><Route path="history" element={<History/>}/><Route path="settings" element={<Settings/>}/></Route><Route path="*" element={<Empty title="A different path awaits." description="This page could not be found. Your workspace is just a step away."><Action to="/workspace">Return to workspace</Action></Empty>}/></Routes></Suspense><Toaster richColors position="bottom-right" closeButton/></MotionConfig>}
export default function App(){return <StoreProvider><BrowserRouter><Content/></BrowserRouter></StoreProvider>}
