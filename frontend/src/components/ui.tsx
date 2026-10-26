import {forwardRef,type ButtonHTMLAttributes,type ReactNode} from 'react';
import {Slot} from '@radix-ui/react-slot';
import * as Dialog from '@radix-ui/react-dialog';
import {cva,type VariantProps} from 'class-variance-authority';
import {clsx} from 'clsx';
import {twMerge} from 'tailwind-merge';
import {X,ArrowUpRight,Check,ArrowRight} from 'lucide-react';
import {Link} from 'react-router-dom';
export function cn(...v:Parameters<typeof clsx>){return twMerge(clsx(v))}
const buttonVariants=cva('btn',{variants:{variant:{default:'btn-primary',secondary:'btn-secondary',ghost:'btn-ghost',danger:'btn-danger'},size:{default:'',sm:'btn-sm',icon:'btn-icon'}},defaultVariants:{variant:'default',size:'default'}});
export const Button=forwardRef<HTMLButtonElement,ButtonHTMLAttributes<HTMLButtonElement>&VariantProps<typeof buttonVariants>&{asChild?:boolean}>(({className,variant,size,asChild,...props},ref)=>{const Comp=asChild?Slot:'button';return <Comp className={cn(buttonVariants({variant,size}),className)} ref={ref} {...props}/>});
Button.displayName='Button';
export function Action({to,children,secondary=false}:{to:string;children:ReactNode;secondary?:boolean}){return <Button asChild variant={secondary?'secondary':'default'}><Link to={to}>{children}<ArrowUpRight size={16}/></Link></Button>}
export function Badge({children,tone='neutral'}:{children:ReactNode;tone?:string}){return <span className={'badge '+tone}>{children}</span>}
export function PageHeader({eyebrow,title,description,action}:{eyebrow:string;title:string;description:string;action?:ReactNode}){return <header className="page-heading"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p></div>{action}</header>}
export function Panel({title,subtitle,children,className='',action}:{title?:string;subtitle?:string;children:ReactNode;className?:string;action?:ReactNode}){return <section className={'panel '+className}>{title&&<div className="panel-head"><div><h2>{title}</h2>{subtitle&&<p>{subtitle}</p>}</div>{action}</div>}{children}</section>}
export function Modal({open,onOpenChange,title,description,children}:{open:boolean;onOpenChange:(v:boolean)=>void;title:string;description:string;children:ReactNode}){return <Dialog.Root open={open} onOpenChange={onOpenChange}><Dialog.Portal><Dialog.Overlay className="dialog-overlay"/><Dialog.Content className="dialog"><Dialog.Title>{title}</Dialog.Title><Dialog.Description>{description}</Dialog.Description><Dialog.Close className="dialog-close" aria-label="Close dialog"><X size={20}/></Dialog.Close>{children}</Dialog.Content></Dialog.Portal></Dialog.Root>}
export function Confirm({open,onOpenChange,title,description,onConfirm}:{open:boolean;onOpenChange:(v:boolean)=>void;title:string;description:string;onConfirm:()=>void}){return <Modal {...{open,onOpenChange,title,description}}><div className="dialog-actions"><Button variant="secondary" onClick={()=>onOpenChange(false)}>Cancel</Button><Button variant="danger" onClick={()=>{onConfirm();onOpenChange(false)}}>Confirm</Button></div></Modal>}
export function Empty({title,description,children}:{title:string;description:string;children?:ReactNode}){return <div className="empty"><div className="empty-symbol">↗</div><h2>{title}</h2><p>{description}</p>{children}</div>}
export function Progress({value,label}:{value:number;label?:string}){return <div className="progress-wrap">{label&&<div className="spread"><span>{label}</span><strong>{value}%</strong></div>}<div role="progressbar" aria-label={label||'Progress'} aria-valuenow={value} aria-valuemin={0} aria-valuemax={100} className="progress"><span style={{width:value+'%'}}/></div></div>}
export function Mark(){return <svg viewBox="0 0 40 40" className="brand-mark" aria-hidden="true"><rect width="40" height="40" rx="11" fill="currentColor"/><path d="M12 29V11h9a6 6 0 0 1 0 12H12m9 0 8 6M12 18h17" stroke="white" strokeWidth="2.8" fill="none"/></svg>}
export function Brand(){return <Link className="brand" to="/" aria-label="RADIX home"><Mark/><span>RADIX<small>TALENT MATCH</small></span></Link>}
export function TextLink({to,children}:{to:string;children:ReactNode}){return <Link className="text-link" to={to}>{children}<ArrowRight size={15}/></Link>}
export function Status({status}:{status:string}){return <Badge tone={status.toLowerCase()}>{status==='Matched'?<Check size={12}/>:<span className="status-dot"/>}{status}</Badge>}
