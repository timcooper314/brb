'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Router from 'next/router';
import styles from '../Brews.module.css';

export default function DeleteBrew(params: any) {
    // const [isDeleted, setIsDeleted] = useState(false);
    const brewId = params.brewId;

    const router = useRouter();

    const deleteBrew = async () => {
        console.log(`Deleting brew ${brewId}...`);
        await fetch(`https://md1o52y8qj.execute-api.ap-southeast-2.amazonaws.com/prod/brews/${brewId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        // setIsDeleted(true);
        router.refresh();
        router.push("/brews/")

    };
    return (
        <button className={styles.deletebutton} onClick={deleteBrew}>
            Delete Brew
        </button>
    );
}