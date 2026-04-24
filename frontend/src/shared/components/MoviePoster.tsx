import { useState } from 'react';

type MoviePosterProps = {
  src: string | null;
  alt: string;
  className?: string;
};

export function MoviePoster({ src, alt, className = '' }: MoviePosterProps) {
  const [imageFailed, setImageFailed] = useState(false);

  if (!src || imageFailed) {
    return (
      <div
        aria-label={`${alt} poster unavailable`}
        className={`flex aspect-[2/3] items-center justify-center rounded-[1.5rem] bg-slate-900 px-6 text-center text-sm text-slate-300 ${className}`}
      >
        Poster unavailable
      </div>
    );
  }

  return (
    <img
      alt={alt}
      className={`aspect-[2/3] rounded-[1.5rem] object-cover ${className}`}
      loading="lazy"
      onError={() => setImageFailed(true)}
      src={src}
    />
  );
}
