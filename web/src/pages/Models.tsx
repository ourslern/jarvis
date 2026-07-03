import { useEffect, useState } from "react";
import { Header } from "../components/layout/Header";
import { Card } from "../components/Card";
import { getModels, ollamaAction } from "../api/jarvis";

export function Models() {

    const [models,setModels]=useState<any>(null);
    const [busy,setBusy]=useState("");

    async function refresh(){
        setModels(await getModels());
    }

    useEffect(()=>{
        refresh();
    },[]);

    async function run(action:string,name:string){

        setBusy(`${action}:${name}`);

        try{

            await ollamaAction(action,name);

            await refresh();

        }finally{

            setBusy("");

        }

    }

    return(

<>

<Header
title="Ollama Control Center"
subtitle="Manage local models"
/>

<section className="model-grid">

{models?.models?.map((m:any)=>{

const running=models?.running?.find(
(r:any)=>r.name===m.name
);

return(

<Card
key={m.name}
title={m.name}
>

<p>

Size

{m.size_gb} GB

</p>

{running?

<div className="badge green">

Loaded

</div>

:

<div className="badge gray">

Not Loaded

</div>

}

<div className="button-row">

{running?

<button
disabled={busy!==""}
onClick={()=>run("unload",m.name)}
>

Unload

</button>

:

<button
disabled={busy!==""}
onClick={()=>run("load",m.name)}
>

Load

</button>

}

<button
disabled={busy!==""}
onClick={()=>run("pull",m.name)}
>

Update

</button>

<button
className="danger"

disabled={busy!==""}

onClick={()=>{

if(confirm(

`Delete ${m.name}?`

))

run("delete",m.name);

}}

>

Delete

</button>

</div>

</Card>

);

})}

</section>

</>

);

}
