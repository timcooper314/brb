import styles from '../Brews.module.css';


// can also prerender all brews using generateStaticParmas
async function getBrew(brewId: string) {
    //console.log(`Fetching brew ${brewId}`)
    const res = await fetch(
        `https://md1o52y8qj.execute-api.ap-southeast-2.amazonaws.com/prod/brews/${brewId}`,
        {
            next: { revalidate: 60 },
        }
    );
    const data = await res.json();
    return data;
}


export default async function BrewPage({ params }: any) {
    const brew = await getBrew(params.brewId);
    return (
        <div>
            <h1>{brew.name}</h1>
            <div className={styles.brew}>
                <h3>{brew.hops}</h3>
                <h3>{brew.grain}</h3>
                <h3>{brew.yeast}</h3>
            </div>
        </div>
    );
}