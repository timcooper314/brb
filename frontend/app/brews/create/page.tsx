'use client';

import { useState } from 'react';

export default function CreateBrew() {
    const [name, setName] = useState('');
    const [brewDate, setBrewDate] = useState('');
    const [grain, setGrain] = useState('');
    const [hops, setHops] = useState('');
    const [yeast, setYeast] = useState('');

    const create = async () => {
        console.log(`Pouring new brew...`);
        const newBrew = {
            name,
            brewDate,
            hops,
            grain,
            yeast,
        };
        console.log(newBrew);
        await fetch(`https://md1o52y8qj.execute-api.ap-southeast-2.amazonaws.com/prod/brews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newBrew),
        });
        console.log("Created!");
        setName('');
        setBrewDate('');
        setGrain('');
        setHops('');
        setYeast('');
    }

    return (
        <form onSubmit={create}>
            <h3>Create a new Brew</h3>
            <label>Brew Name:</label>
            <input
                type="text"
                placeholder="Mozacca Pale"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <label>Brew Date:</label>
            <input
                type="text"
                placeholder="2022-06-14"
                value={brewDate}
                onChange={(e) => setBrewDate(e.target.value)}
            />
            <label>Grain:</label>
            <input
                type="text"
                placeholder="Maris Otter, Crystal light"
                value={grain}
                onChange={(e) => setGrain(e.target.value)}
            />
            <label>Hops:</label>
            <input
                type="text"
                placeholder="Mosaic, Azacca"
                value={hops}
                onChange={(e) => setHops(e.target.value)}
            />
            <label>Yeast:</label>
            <input
                type="text"
                placeholder="US-05"
                value={yeast}
                onChange={(e) => setYeast(e.target.value)}
            />
            <button type="submit">
                Pour Brew
            </button>
        </form>
    );
}