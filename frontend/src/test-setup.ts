import '@testing-library/jest-dom/vitest';
import {vi} from 'vitest';
Object.defineProperty(window,'matchMedia',{writable:true,value:vi.fn().mockImplementation(q=>({matches:false,media:q,addEventListener:vi.fn(),removeEventListener:vi.fn()}))});
window.scrollTo=vi.fn();
globalThis.ResizeObserver=class {observe(){} unobserve(){} disconnect(){}};

