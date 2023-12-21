import Link from "next/link";
import React from "react";
import { createClient } from "@/app/lib/utils/supabase/server";
import "./signup-form.css";
import { cookies, headers } from "next/headers";
import { redirect } from "next/navigation";

export default function SignUpForm({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  const handleSignUp = async (formData: FormData) => {
    "use server";

    const origin = headers().get("origin");
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    const cookieStore = cookies();
    const supabase = createClient(cookieStore);

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${origin}/auth/callback`,
      },
    });

    if (error) {
      return redirect(`/account/signup?message=${error.message}`);
    }

    formData.set("email", "");

    return redirect(
      "/account/signup?message=Check your email to continue sign in process"
    );
  };

  return (
    <div className="auth-container">
      <div className="auth-container__title-section">
        <h2 className="auth-container__title">Create your account</h2>
      </div>
      <div className="auth-container__form-section">
        <form className="auth-form" action={handleSignUp}>
          <div className="auth-form__name-section">
            {/* Name Input */}
            <div className="auth-form__field">
              <label htmlFor="first_name" className="auth-form__label">
                First name
              </label>
              <div className="auth-form__input-container">
                <input
                  id="first_name"
                  name="first_name"
                  type="first_name"
                  required
                  className="auth-form__input auth-form__name-input"
                />
              </div>
            </div>

            <div className="auth-form__field">
              <label htmlFor="last_name" className="auth-form__label">
                Last name
              </label>
              <div className="auth-form__input-container">
                <input
                  id="last_name"
                  name="last_name"
                  type="last_name"
                  required
                  className="auth-form__input auth-form__name-input"
                />
              </div>
            </div>
          </div>
          {/* Email Input */}
          <div className="auth-form__field">
            <label htmlFor="email" className="auth-form__label">
              Email address
            </label>
            <div className="auth-form__input-container">
              <input
                id="email"
                name="email"
                type="email"
                required
                className="auth-form__input auth-form__credentials-input"
              />
            </div>
          </div>

          {/* Password Input */}
          <div className="auth-form__field">
            <div className="auth-form__password-header">
              <label htmlFor="password" className="auth-form__label">
                Password
              </label>
            </div>
            <div className="auth-form__input-container">
              <input
                id="password"
                name="password"
                type="password"
                required
                className="auth-form__input auth-form__credentials-input"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="auth-form__submit-container">
            <button type="submit" className="auth-form__submit-button">
              Sign up
            </button>
          </div>
          {/* {signUpError && (
            <p className="auth-form__error-text">Error: {signUpError}</p>
          )} */}
          {searchParams?.message && (
            <p className="auth-form__error-text">{searchParams.message}</p>
          )}
        </form>
        <p className="auth-container__footer-text">
          Already a member?&nbsp;
          <Link href="/account/login" className="auth-form__link">
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
}
