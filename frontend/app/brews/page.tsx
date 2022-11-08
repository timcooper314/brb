import Link from 'next/link';
import styles from './Brews.module.css'
import CreateBrew from './CreateBrew';


async function getBrews() {
    console.log('Fetching all brews...')
    const res = await fetch('https://md1o52y8qj.execute-api.ap-southeast-2.amazonaws.com/prod/brews'); // can include cache: no-store option
    const data = await res.json();
    return data?.brews as any[];
}


export default async function BrewsPage() {
    const brews = await getBrews();
    return (
        <div>
            <h1>Brews</h1>
            <div className={styles.grid}>
                {brews?.map((brew) => {
                    return <Brew key={brew.brewId} brew={brew} />;
                })}
            </div>

            <CreateBrew />
        </div>
    );
}

function Brew({ brew }: any) {
    const { brewId, name, brewDate, grain, hops, yeast } = brew || {};

    return (
        <Link href={`/brews/${brewId}`}>
            <div className={styles.brew}>
                <h2>{name}</h2>
                <h5>{hops}</h5>
                <p>{brewDate}</p>
            </div>
        </Link>
    );
}
