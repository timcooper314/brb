import Link from 'next/link';
import './globals.css';
import Image from 'next/image'
import BrbWhiteLogo from '../public/Blue-Room-Brewing-logo-White.png'
// Shared by all pages - good place to add a global navbar e.g.
export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html>
            <body>
                <main>
                    <nav>
                        <Link href="/">
                            <Image src={BrbWhiteLogo} alt="BRB logo" width={60} />
                        </Link>
                        <Link href="/">
                            Home
                        </Link>
                        <Link href="/brews">
                            Brews
                        </Link>
                    </nav>
                    {children}
                </main>
            </body>
        </html>
    );
}