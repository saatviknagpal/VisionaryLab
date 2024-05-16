"use client"

import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
  } from "@/components/ui/sheet"
import { navLinks } from "@/constants"
import { SignedIn, SignedOut, UserButton } from "@clerk/nextjs"
import Image from "next/image"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "../ui/button"
  
const MobileNav = () => {
    const pathname = usePathname();
  return (
    <header className="header">
        <Link href="/" className="flex items-center gap-2 md:py-2">
            <Image src="/assets/images/logo-text.png" alt="logo" width={55} height={30} className="m-auto" />
        </Link>
        <nav className="flex gap-2">
            <SignedIn>
                <UserButton afterSignOutUrl="/" showName />
                <Sheet>
  <SheetTrigger><Image src="/assets/icons/menu.svg" alt="menu" width={32} height={32} className="cursor-pointer"/></SheetTrigger>
  <SheetContent className="sheet-content sm:w-64">
    <>
        <Image src="/assets/images/logo-text.png" alt="logo" width={100} height={28} className="m-auto" />
        <ul className='sidebar-nav_elements'>
                    {navLinks.map((link) => {
                        const isActive = link.route === pathname

                        return (
                            <li key = {link.route} 
                            className={`${isActive && 'gradient-text'} p-18 flex whitespace-nowrap text-dark-700`}>
                                <Link className='sidebar-link cursor-pointer' href={link.route}>
                                    <Image src = {link.icon} alt="logo" width={24} height={24}/>
                                        {link.label}
                                </Link>
                            </li>
                    )})}
                    <li className='flex-center cursor-pointer gap-2 p-4'>
                        <UserButton afterSignOutUrl='/' showName />
                    </li>
                    </ul>
    </>
  </SheetContent>
</Sheet>

            </SignedIn>

            <SignedOut>

            <Button asChild className='button bg-purple-gradient bg-cover'>
                        <Link href="/sign-in">Login</Link>
                    </Button>
            </SignedOut>
        </nav>
    </header>
  )
}

export default MobileNav