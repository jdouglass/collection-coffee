import SignUpForm from "@/app/components/SignUpForm/SignUpForm";

export default function SignUpPage({
  searchParams,
}: {
  searchParams: { message: string };
}) {
  return <SignUpForm searchParams={searchParams} />;
}
