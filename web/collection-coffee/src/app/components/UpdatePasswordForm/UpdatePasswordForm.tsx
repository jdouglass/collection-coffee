import "./update-password-form.css";
import { redirect } from "next/navigation";
import { createClient } from "@/app/lib/utils/supabase/server";
import { cookies } from "next/headers";

export default function UpdatePasswordForm({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  const handlePasswordUpdate = async (formData: FormData) => {
    "use server";

    const cookieStore = cookies();
    const supabase = createClient(cookieStore);
    console.log(formData.get("password") as string);
    console.log(formData.get("passwordConfirm") as string);

    if (
      (formData.get("password") as string) ===
      (formData.get("passwordConfirm") as string)
    ) {
      const { error } = await supabase.auth.updateUser({
        password: formData.get("password") as string,
      });

      if (error) {
        return redirect(
          "/account/update-password?message=Passwords do no match"
        );
      }

      return redirect("/account/update-password?message=Success");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-container__title-section">
        <h2 className="auth-container__title">Create your new password</h2>
      </div>

      <div className="auth-container__form-section">
        <form className="auth-form" action={handlePasswordUpdate}>
          {/* Password Input */}
          <div className="auth-form__field">
            <label htmlFor="password" className="auth-form__label">
              Password
            </label>
            <div className="auth-form__input-container">
              <input
                id="password"
                name="password"
                type="password"
                required
                className="auth-form__input"
              />
            </div>
          </div>

          {/* Confirm Password Input */}
          <div className="auth-form__field">
            <div className="auth-form__password-header">
              <label htmlFor="password" className="auth-form__label">
                Confirm password
              </label>
            </div>
            <div className="auth-form__input-container">
              <input
                id="passwordConfirm"
                name="passwordConfirm"
                type="password"
                required
                className="auth-form__input"
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="auth-form__submit-container">
            <button type="submit" className="auth-form__submit-button">
              Update password
            </button>
          </div>
          {/* {loginError && (
            <p className="auth-form__error-text">Error: {loginError}</p>
          )} */}
          {searchParams?.message && (
            <p className="auth-form__error-text">{searchParams.message}</p>
          )}
        </form>
      </div>
    </div>
  );
}
