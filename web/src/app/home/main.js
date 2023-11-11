"use client";
import Image from "next/image";
import { Transition } from "@headlessui/react";
import { ArrowBigRightDash, LucideLightbulb } from "lucide-react";
import useTranslation from "next-translate/useTranslation";

export default function Hero() {
  const { t } = useTranslation("common");
  return (
    <section className="max-w-7xl mx-auto flex md:flex-row flex-col-reverse p-5">
      {/* Illustration behind hero content */}
      <div className="w-full md:w-1/2">
        <div
          className="hidden md:absolute left-1/2 transform -translate-x-1/2 bottom-0 pointer-events-none -z-1 "
          aria-hidden="true"
        >
          <svg
            width="1260"
            height="578"
            viewBox="0 0 1360 578"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <linearGradient
                x1="50%"
                y1="0%"
                x2="50%"
                y2="100%"
                id="illustration-01"
              >
                <stop stopColor="#FFF" offset="0%" />
                <stop stopColor="#EAEAEA" offset="77.402%" />
                <stop stopColor="#DFDFDF" offset="100%" />
              </linearGradient>
            </defs>
            <g fill="url(#illustration-01)" fillRule="evenodd">
              <circle cx="1232" cy="128" r="128" />
              <circle cx="155" cy="443" r="64" />
            </g>
          </svg>
        </div>
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          {/* Hero content */}
          <div className="p-3 md:py-14 ">
            {/* Section header */}
            <div className="text-center pb-12 md:pb-16">
              <h1
                className="text-4xl md:text-5xl font-extrabold leading-tighter tracking-tighter mb-4"
                data-aos="zoom-y-out"
              >
                {t("we")} <br /> {t("build")} <br />
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-green-500 to-teal-400 text-5xl md:text-6xl">
                  {t("dreams")}
                </span>
              </h1>
              <div className="max-w-3xl mx-auto">
                <p
                  className="text-xl text-gray-600 dark:text-gray-200 mb-8"
                  data-aos="zoom-y-out"
                  data-aos-delay="150"
                >
                  {t("description")}
                </p>
                <div
                  className="max-w-xs mx-auto sm:max-w-none sm:flex sm:justify-center"
                  data-aos="zoom-y-out"
                  data-aos-delay="300"
                >
                  <div>
                    <a
                      className="btn text-white bg-blue-600 hover:bg-blue-700 w-full mb-4 sm:w-auto sm:mb-0 gap-2"
                      href="/auth/signin"
                    >
                      <LucideLightbulb /> {t("start")}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="w-full md:w-1/2 ">
        <Transition
          show={true}
          appear={true}
          className="w-full"
          enter="transition ease-in-out duration-700 transform order-first"
          enterFrom="opacity-0 translate-y-16"
          enterTo="opacity-100 translate-y-0"
          leave="transition ease-in-out duration-300 transform absolute"
          leaveFrom="opacity-100 translate-y-0"
          leaveTo="opacity-0 -translate-y-16"
          unmount={false}
        >
        <Image
          src="/room.png"
          height={1024}
          width={1024}
          alt="hero"
          className=""
          priority
        />
        </Transition>
      </div>
    </section>
  );
}
