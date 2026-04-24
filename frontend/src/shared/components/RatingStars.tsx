type RatingStarsProps = {
  rating: number | null;
};

export function RatingStars({ rating }: RatingStarsProps) {
  if (rating == null) {
    return (
      <span className="text-sm text-[color:var(--muted)]">Not yet rated</span>
    );
  }

  const rounded = Math.round(rating);

  return (
    <span
      aria-label={`Rated ${rating.toFixed(1)} out of 5`}
      className="text-sm text-amber-600"
    >
      {'★'.repeat(rounded)}
      <span className="text-slate-300">{'★'.repeat(5 - rounded)}</span>
      <span className="ml-2 text-[color:var(--muted)]">
        {rating.toFixed(1)}
      </span>
    </span>
  );
}
