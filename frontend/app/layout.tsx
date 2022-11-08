import Link from 'next/link';
import './globals.css';


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