import { createClient } from "@/app/lib/utils/supabase/server";
import Link from "next/link";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import "./auth-button.css";
import { LogoutButton } from "../LogoutButton/LogoutButton";

export default async function AuthButton() {
  const cookieStore = cookies();
  const supabase = createClient(cookieStore);

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const signOut = async () => {
    "use server";

    const cookieStore = cookies();
    const supabase = createClient(cookieStore);
    await supabase.auth.signOut();
    return redirect("/");
  };

  return user ? (
    <div className="flex items-center gap-4">
      <form action={signOut}>
        <LogoutButton />
      </form>
    </div>
  ) : (
    <div className="auth__button--container">
      <Link href="/account/login" className="auth__button sign-in__button">
        Sign in
      </Link>
      <Link href="/account/signup" className="auth__button sign-up__button">
        Sign up
      </Link>
    </div>
  );
}
