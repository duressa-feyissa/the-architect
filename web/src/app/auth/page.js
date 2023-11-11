import Image from "next/image";
import Link from "next/link";
import { UserAuthForm } from "./form";
import useTranslation from "next-translate/useTranslation";

export const metadata = {
  title: "Authentication",
  description: "Authentication forms built using the components.",
};

export default function AuthenticationPage() {
  const { t } = useTranslation("common");

  return (
    <>
      <div className="container relative min-h-screen max-h-screen flex-col items-center justify-center grid lg:max-w-none lg:grid-cols-2 lg:px-0">
        <Link
          href="/auth/signup"
          className="absolute right-4 top-4 md:right-8 md:top-8"
        >
          {t("pa_new")}
        </Link>
        <div className="relative hidden h-full flex-col bg-muted p-10 text-white dark:border-r lg:flex">
          <div className="absolute inset-0 bg-zinc-900" />
          <div className="relative z-20 flex flex-col items-center  text-lg font-medium">
            <span className="flex gap-4 items-center justify-center p-3">
              <Image
                src="/logo.svg"
                alt=""
                width={40}
                height={40}
                priority
                className="w-auto"
              />
              The Architect by Innovate Fusion
              <Image src="/if.png" alt="" width={80} height={80} />
            </span>
            <div className="flex items-center justify-center">
              <Image
                src="/house.jpg"
                width={1280}
                height={843}
                alt="Authentication"
                className="block w-[80%]"
                priority
              />
              <Image
                src="/house.jpg"
                width={1280}
                height={843}
                alt="Authentication"
                className="hidden dark:block"
                priority
              />
            </div>
          </div>
        </div>
        <div className="lg:p-8">
          <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
            <div className="flex flex-col space-y-2 text-center">
              <h1 className="text-2xl font-semibold tracking-tight">
                {t("pa_login")}
              </h1>
            </div>
            <UserAuthForm />
            <p className="px-8 text-center text-sm text-muted-foreground">
              {t("pa_continue")}
              <Link
                href="/terms"
                className="underline underline-offset-4 hover:text-primary"
              >
                {t("pa_service")}
              </Link>
              {t("pa_a")}
              <Link
                href="/privacy"
                className="underline underline-offset-4 hover:text-primary"
              >
                {t("su_privacy")}
              </Link>
              .
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
